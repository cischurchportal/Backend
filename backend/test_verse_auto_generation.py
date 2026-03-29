"""
Test: Auto-generation of daily Bible verse
==========================================
Tests the full flow:
  1. External API fetch (bible-api.com)
  2. Deterministic fallback when API is down
  3. DB cache — second call returns saved verse, no external call
  4. Admin override — admin-saved verse takes priority
  5. Home page endpoint returns verse

Run from Backend/backend/:
    python test_verse_auto_generation.py
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))

# ── helpers ──────────────────────────────────────────────────────────────────

PASS = "✅ PASS"
FAIL = "❌ FAIL"
results: list[tuple[str, bool, str]] = []


def record(name: str, passed: bool, detail: str = ""):
    results.append((name, passed, detail))
    status = PASS if passed else FAIL
    print(f"  {status}  {name}" + (f"\n         {detail}" if detail else ""))


# ── Test 1: Deterministic fallback picks same verse for same date ─────────────

def test_deterministic_fallback():
    print("\n[1] Deterministic fallback consistency")
    from app.services.church_service import _pick_for_date, FALLBACK_VERSES

    today = date.today().isoformat()
    idx1 = _pick_for_date(today)
    idx2 = _pick_for_date(today)
    record(
        "Same date always returns same index",
        idx1 == idx2,
        f"index={idx1}, verse='{FALLBACK_VERSES[idx1]['reference']}'"
    )

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow  = (date.today() + timedelta(days=1)).isoformat()
    idx_y = _pick_for_date(yesterday)
    idx_t = _pick_for_date(tomorrow)
    record(
        "Different dates return different indices (usually)",
        not (idx_y == idx1 == idx_t),   # all three same would be suspicious
        f"yesterday={idx_y}, today={idx1}, tomorrow={idx_t}"
    )

    record(
        "Index is within FALLBACK_VERSES bounds",
        0 <= idx1 < len(FALLBACK_VERSES),
        f"len(FALLBACK_VERSES)={len(FALLBACK_VERSES)}"
    )


# ── Test 2: External API fetch (live, may be skipped if offline) ──────────────

async def test_external_api_live():
    print("\n[2] External API fetch (live network call)")
    from app.services.church_service import _fetch_from_bible_api

    today = date.today().isoformat()
    try:
        result = await _fetch_from_bible_api(today)
        if result:
            record(
                "bible-api.com returned a verse",
                True,
                f"reference='{result['reference']}', text='{result['verse'][:60]}...'"
            )
            record("Verse text is non-empty",  bool(result.get("verse")))
            record("Reference is non-empty",   bool(result.get("reference")))
        else:
            record("bible-api.com returned a verse", False, "Got None — API may be down, fallback will be used")
    except Exception as e:
        record("bible-api.com returned a verse", False, f"Exception: {e}")


# ── Test 3: API failure → fallback verse is used ─────────────────────────────

async def test_fallback_on_api_failure():
    print("\n[3] Fallback when external API fails")
    from app.services.church_service import ChurchService, FALLBACK_VERSES

    today = date.today().isoformat()

    # Mock: DB has no verse, API raises an exception
    with patch("app.services.church_service._fetch_from_bible_api", new_callable=AsyncMock) as mock_api, \
         patch.object(ChurchService, "__init__", lambda self: setattr(self, "church_repo", MagicMock())):

        mock_api.return_value = None  # API returns nothing

        svc = ChurchService.__new__(ChurchService)
        svc.church_repo = MagicMock()
        svc.church_repo.get_verse_of_day.return_value = None   # nothing in DB
        svc.church_repo.create_verse.side_effect = lambda d: {**d, "id": 99}

        result = await svc.get_or_auto_create_verse_of_day(today)

        record("Returns a verse even when API fails", result is not None)
        if result:
            record(
                "Fallback verse is from curated list",
                result["verse"] in [v["verse"] for v in FALLBACK_VERSES],
                f"reference='{result.get('reference')}'"
            )
            record("Verse saved to DB",  svc.church_repo.create_verse.called)


# ── Test 4: DB cache — second call skips API ─────────────────────────────────

async def test_db_cache():
    print("\n[4] DB cache — second request skips external API")
    from app.services.church_service import ChurchService

    today = date.today().isoformat()
    cached_verse = {
        "id": 1, "date": today,
        "verse": "The Lord is my shepherd, I lack nothing.",
        "reference": "Psalm 23:1",
        "commentary": None, "is_active": True
    }

    with patch("app.services.church_service._fetch_from_bible_api", new_callable=AsyncMock) as mock_api:
        svc = ChurchService.__new__(ChurchService)
        svc.church_repo = MagicMock()
        svc.church_repo.get_verse_of_day.return_value = cached_verse  # already in DB

        result = await svc.get_or_auto_create_verse_of_day(today)

        record("Returns cached verse from DB",       result == cached_verse)
        record("External API was NOT called",        not mock_api.called)
        record("DB create was NOT called",           not svc.church_repo.create_verse.called)


# ── Test 5: Admin override takes priority ────────────────────────────────────

async def test_admin_override():
    print("\n[5] Admin override takes priority over auto-generated verse")
    from app.services.church_service import ChurchService

    today = date.today().isoformat()
    admin_verse = {
        "id": 5, "date": today,
        "verse": "Custom verse set by admin.",
        "reference": "Admin 1:1",
        "commentary": "Admin commentary",
        "is_active": True
    }

    with patch("app.services.church_service._fetch_from_bible_api", new_callable=AsyncMock) as mock_api:
        svc = ChurchService.__new__(ChurchService)
        svc.church_repo = MagicMock()
        svc.church_repo.get_verse_of_day.return_value = admin_verse  # admin already saved one

        result = await svc.get_or_auto_create_verse_of_day(today)

        record("Admin verse is returned",            result["reference"] == "Admin 1:1")
        record("External API was NOT called",        not mock_api.called)
        record("Admin commentary preserved",         result.get("commentary") == "Admin commentary")


# ── Test 6: New verse is saved to DB on first visit ──────────────────────────

async def test_verse_saved_to_db():
    print("\n[6] Auto-generated verse is saved to DB")
    from app.services.church_service import ChurchService

    today = date.today().isoformat()
    api_verse = {
        "verse": "For God so loved the world...",
        "reference": "John 3:16",
        "commentary": None
    }
    saved_verse = {**api_verse, "id": 10, "date": today, "is_active": True}

    with patch("app.services.church_service._fetch_from_bible_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = api_verse

        svc = ChurchService.__new__(ChurchService)
        svc.church_repo = MagicMock()
        svc.church_repo.get_verse_of_day.return_value = None   # nothing in DB yet
        svc.church_repo.create_verse.return_value = saved_verse

        result = await svc.get_or_auto_create_verse_of_day(today)

        record("create_verse was called",            svc.church_repo.create_verse.called)
        call_args = svc.church_repo.create_verse.call_args[0][0]
        record("Saved with correct date",            call_args.get("date") == today)
        record("Saved with correct reference",       call_args.get("reference") == "John 3:16")
        record("Saved with is_active=True",          call_args.get("is_active") is True)
        record("Returned verse has DB id",           result.get("id") == 10)


# ── Test 7: Home page data includes verse ────────────────────────────────────

async def test_home_page_includes_verse():
    print("\n[7] Home page data includes verse_of_day")
    from app.services.church_service import ChurchService

    today = date.today().isoformat()
    mock_verse = {
        "id": 1, "date": today,
        "verse": "Be still, and know that I am God.",
        "reference": "Psalm 46:10",
        "is_active": True
    }

    svc = ChurchService.__new__(ChurchService)
    svc.church_repo = MagicMock()
    svc.church_repo.get_church_settings.return_value = {"church_name": "Test Church"}
    svc.church_repo.get_priests.return_value = []
    svc.church_repo.get_verse_of_day.return_value = mock_verse
    svc.church_repo.get_active_announcements.return_value = []
    svc.church_repo.get_service_timings.return_value = []
    svc.church_repo.get_today_celebrations.return_value = []
    svc.church_repo.get_upcoming_celebrations.return_value = []

    data = await svc.get_home_page_data()

    record("home data has 'verse_of_day' key",       "verse_of_day" in data)
    record("verse_of_day is not None",               data.get("verse_of_day") is not None)
    record("verse reference matches",                data["verse_of_day"]["reference"] == "Psalm 46:10")
    record("home data has all expected keys",
           all(k in data for k in ["church_settings", "priests", "verse_of_day",
                                    "announcements", "service_timings", "today_celebrations"]))


# ── Test 8: Different dates get different auto-verses ────────────────────────

async def test_different_dates_different_verses():
    print("\n[8] Different dates produce different verses (fallback)")
    from app.services.church_service import ChurchService, FALLBACK_VERSES

    dates = [
        (date.today() - timedelta(days=i)).isoformat()
        for i in range(5)
    ]
    seen_refs = set()

    with patch("app.services.church_service._fetch_from_bible_api", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = None  # force fallback

        for d in dates:
            svc = ChurchService.__new__(ChurchService)
            svc.church_repo = MagicMock()
            svc.church_repo.get_verse_of_day.return_value = None
            svc.church_repo.create_verse.side_effect = lambda data: {**data, "id": 1}

            result = await svc.get_or_auto_create_verse_of_day(d)
            if result:
                seen_refs.add(result["reference"])

    record(
        "Multiple dates produce multiple distinct verses",
        len(seen_refs) > 1,
        f"Distinct references across 5 days: {seen_refs}"
    )


# ── Runner ────────────────────────────────────────────────────────────────────

async def run_all():
    print("=" * 60)
    print("  Bible Verse Auto-Generation — Test Suite")
    print("=" * 60)

    test_deterministic_fallback()
    await test_external_api_live()
    await test_fallback_on_api_failure()
    await test_db_cache()
    await test_admin_override()
    await test_verse_saved_to_db()
    await test_home_page_includes_verse()
    await test_different_dates_different_verses()

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    passed = sum(1 for _, ok, _ in results if ok)
    total  = len(results)
    for name, ok, detail in results:
        print(f"  {'✅' if ok else '❌'}  {name}")

    print(f"\n  {passed}/{total} tests passed")
    if passed == total:
        print("  🎉 All tests passed!")
    else:
        failed = [name for name, ok, _ in results if not ok]
        print(f"  ⚠️  Failed: {', '.join(failed)}")
    print("=" * 60)
    return passed == total


if __name__ == "__main__":
    ok = asyncio.run(run_all())
    sys.exit(0 if ok else 1)
