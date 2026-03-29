from typing import List, Optional, Dict, Any
from datetime import datetime, date
import hashlib
import httpx
import logging
from app.repositories.church_repository import ChurchRepository

logger = logging.getLogger(__name__)

# Curated list of well-known Bible verses — one is picked deterministically by date
# so the same date always maps to the same verse even if the external API is down
FALLBACK_VERSES = [
    {"verse": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.", "reference": "John 3:16"},
    {"verse": "I can do all this through him who gives me strength.", "reference": "Philippians 4:13"},
    {"verse": "The Lord is my shepherd, I lack nothing.", "reference": "Psalm 23:1"},
    {"verse": "Trust in the Lord with all your heart and lean not on your own understanding.", "reference": "Proverbs 3:5"},
    {"verse": "Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.", "reference": "Joshua 1:9"},
    {"verse": "And we know that in all things God works for the good of those who love him.", "reference": "Romans 8:28"},
    {"verse": "The Lord is my light and my salvation — whom shall I fear?", "reference": "Psalm 27:1"},
    {"verse": "Come to me, all you who are weary and burdened, and I will give you rest.", "reference": "Matthew 11:28"},
    {"verse": "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future.", "reference": "Jeremiah 29:11"},
    {"verse": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.", "reference": "Philippians 4:6"},
    {"verse": "The name of the Lord is a fortified tower; the righteous run to it and are safe.", "reference": "Proverbs 18:10"},
    {"verse": "But those who hope in the Lord will renew their strength. They will soar on wings like eagles.", "reference": "Isaiah 40:31"},
    {"verse": "Give thanks to the Lord, for he is good; his love endures forever.", "reference": "Psalm 107:1"},
    {"verse": "Jesus said to him, I am the way and the truth and the life.", "reference": "John 14:6"},
    {"verse": "The Lord bless you and keep you; the Lord make his face shine on you and be gracious to you.", "reference": "Numbers 6:24-25"},
    {"verse": "Cast all your anxiety on him because he cares for you.", "reference": "1 Peter 5:7"},
    {"verse": "Love is patient, love is kind. It does not envy, it does not boast, it is not proud.", "reference": "1 Corinthians 13:4"},
    {"verse": "Even though I walk through the darkest valley, I will fear no evil, for you are with me.", "reference": "Psalm 23:4"},
    {"verse": "Seek first his kingdom and his righteousness, and all these things will be given to you as well.", "reference": "Matthew 6:33"},
    {"verse": "The Lord is close to the brokenhearted and saves those who are crushed in spirit.", "reference": "Psalm 34:18"},
    {"verse": "I have hidden your word in my heart that I might not sin against you.", "reference": "Psalm 119:11"},
    {"verse": "Be still, and know that I am God.", "reference": "Psalm 46:10"},
    {"verse": "With God all things are possible.", "reference": "Matthew 19:26"},
    {"verse": "The Lord your God is with you, the Mighty Warrior who saves.", "reference": "Zephaniah 3:17"},
    {"verse": "Let your light shine before others, that they may see your good deeds and glorify your Father in heaven.", "reference": "Matthew 5:16"},
    {"verse": "I am the resurrection and the life. The one who believes in me will live, even though they die.", "reference": "John 11:25"},
    {"verse": "Delight yourself in the Lord, and he will give you the desires of your heart.", "reference": "Psalm 37:4"},
    {"verse": "No weapon forged against you will prevail.", "reference": "Isaiah 54:17"},
    {"verse": "The steadfast love of the Lord never ceases; his mercies never come to an end.", "reference": "Lamentations 3:22"},
    {"verse": "Ask and it will be given to you; seek and you will find; knock and the door will be opened to you.", "reference": "Matthew 7:7"},
    {"verse": "I praise you because I am fearfully and wonderfully made.", "reference": "Psalm 139:14"},
]

# Rotating list of Bible references to fetch from the external API
# Indexed by day-of-year mod len so each day gets a different verse
BIBLE_REFERENCES = [
    "john+3:16", "philippians+4:13", "psalm+23:1", "proverbs+3:5-6",
    "joshua+1:9", "romans+8:28", "psalm+27:1", "matthew+11:28-30",
    "jeremiah+29:11", "philippians+4:6-7", "isaiah+40:31", "psalm+107:1",
    "john+14:6", "1+peter+5:7", "1+corinthians+13:4-5", "psalm+34:18",
    "matthew+6:33", "psalm+46:10", "matthew+19:26", "zephaniah+3:17",
    "matthew+5:16", "john+11:25-26", "psalm+37:4", "isaiah+54:17",
    "lamentations+3:22-23", "matthew+7:7", "psalm+139:14", "romans+12:2",
    "galatians+5:22-23", "ephesians+2:8-9", "hebrews+11:1", "james+1:17",
]


def _pick_for_date(date_str: str) -> int:
    """Deterministically pick an index from a date string using a hash."""
    h = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    return h % len(FALLBACK_VERSES)


async def _fetch_from_bible_api(date_str: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a verse from bible-api.com (free, no key required).
    Returns a dict with verse/reference/commentary or None on failure.
    """
    try:
        day_of_year = datetime.strptime(date_str, "%Y-%m-%d").timetuple().tm_yday
        ref = BIBLE_REFERENCES[day_of_year % len(BIBLE_REFERENCES)]
        url = f"https://bible-api.com/{ref}?translation=kjv"

        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                verse_text = data.get("text", "").strip().replace("\n", " ")
                reference = data.get("reference", "")
                if verse_text and reference:
                    return {
                        "verse": verse_text,
                        "reference": reference,
                        "commentary": None
                    }
    except Exception as e:
        logger.warning(f"bible-api.com fetch failed for {date_str}: {e}")
    return None


class ChurchService:
    def __init__(self):
        self.church_repo = ChurchRepository()
    
    def get_church_settings(self) -> Optional[Dict[str, Any]]:
        return self.church_repo.get_church_settings()
    
    def update_church_settings(self, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.church_repo.update_church_settings(updates)
    
    def get_priests(self) -> List[Dict[str, Any]]:
        return self.church_repo.get_priests()
    
    def get_priest_by_id(self, priest_id: int) -> Optional[Dict[str, Any]]:
        return self.church_repo.get_priest_by_id(priest_id)
    
    def create_priest(self, priest_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'is_active' not in priest_data:
            priest_data['is_active'] = True
        if 'display_order' not in priest_data:
            existing_priests = self.church_repo.get_priests()
            max_order = max([p.get('display_order', 0) for p in existing_priests], default=0)
            priest_data['display_order'] = max_order + 1
        return self.church_repo.create_priest(priest_data)
    
    def update_priest(self, priest_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.church_repo.update_priest(priest_id, updates)
    
    def delete_priest(self, priest_id: int) -> bool:
        return self.church_repo.delete_priest(priest_id)
    
    def get_verse_of_day(self, date_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get verse for today — returns DB record if exists, else falls back to latest."""
        if not date_str:
            date_str = date.today().isoformat()
        verse = self.church_repo.get_verse_of_day(date_str)
        if not verse:
            verse = self.church_repo.get_latest_verse()
        return verse

    async def get_or_auto_create_verse_of_day(self, date_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get today's verse from DB. If none exists, fetch from bible-api.com,
        fall back to curated list, save to DB, and return it.
        Admin overrides are preserved because they already exist in DB for that date.
        """
        if not date_str:
            date_str = date.today().isoformat()

        # 1. Check DB first — admin override or previously auto-generated
        verse = self.church_repo.get_verse_of_day(date_str)
        if verse:
            return verse

        # 2. Try external API
        fetched = await _fetch_from_bible_api(date_str)

        if fetched:
            verse_data = {
                "date": date_str,
                "verse": fetched["verse"],
                "reference": fetched["reference"],
                "commentary": fetched.get("commentary"),
                "is_active": True
            }
        else:
            # 3. Deterministic fallback from curated list
            idx = _pick_for_date(date_str)
            fallback = FALLBACK_VERSES[idx]
            verse_data = {
                "date": date_str,
                "verse": fallback["verse"],
                "reference": fallback["reference"],
                "commentary": None,
                "is_active": True
            }

        # 4. Save to DB so subsequent requests hit the cache
        try:
            saved = self.church_repo.create_verse(verse_data)
            logger.info(f"Auto-created verse for {date_str}: {verse_data['reference']}")
            return saved
        except Exception as e:
            logger.error(f"Failed to save auto-generated verse: {e}")
            # Return unsaved dict so the page still shows something
            return verse_data

    def create_verse(self, verse_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'is_active' not in verse_data:
            verse_data['is_active'] = True
        if 'date' not in verse_data:
            verse_data['date'] = date.today().isoformat()
        return self.church_repo.create_verse(verse_data)
    
    def update_verse(self, verse_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.church_repo.update_verse(verse_id, updates)
    
    def get_announcements(self) -> List[Dict[str, Any]]:
        return self.church_repo.get_active_announcements()
    
    def create_announcement(self, announcement_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'is_active' not in announcement_data:
            announcement_data['is_active'] = True
        if 'priority' not in announcement_data:
            announcement_data['priority'] = 'medium'
        if 'type' not in announcement_data:
            announcement_data['type'] = 'general'
        return self.church_repo.create_announcement(announcement_data)
    
    def update_announcement(self, announcement_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.church_repo.update_announcement(announcement_id, updates)
    
    def delete_announcement(self, announcement_id: int) -> bool:
        return self.church_repo.delete_announcement(announcement_id)
    
    def get_service_timings(self) -> List[Dict[str, Any]]:
        return self.church_repo.get_service_timings()
    
    def create_service_timing(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'is_active' not in service_data:
            service_data['is_active'] = True
        if 'language' not in service_data:
            service_data['language'] = 'English'
        return self.church_repo.create_service_timing(service_data)
    
    def update_service_timing(self, service_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.church_repo.update_service_timing(service_id, updates)
    
    def delete_service_timing(self, service_id: int) -> bool:
        return self.church_repo.delete_service_timing(service_id)
    
    def get_all_celebrations(self) -> List[Dict[str, Any]]:
        return self.church_repo.get_all_celebrations()

    def get_today_celebrations(self) -> List[Dict[str, Any]]:
        today = date.today().isoformat()
        return self.church_repo.get_today_celebrations(today)
    
    def get_upcoming_celebrations(self, days: int = 7) -> List[Dict[str, Any]]:
        return self.church_repo.get_upcoming_celebrations(days)
    
    def create_celebration(self, celebration_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'is_active' not in celebration_data:
            celebration_data['is_active'] = True
        if 'date' not in celebration_data:
            celebration_data['date'] = date.today().isoformat()
        return self.church_repo.create_celebration(celebration_data)
    
    def update_celebration(self, celebration_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.church_repo.update_celebration(celebration_id, updates)
    
    def delete_celebration(self, celebration_id: int) -> bool:
        return self.church_repo.delete_celebration(celebration_id)
    
    async def get_home_page_data(self) -> Dict[str, Any]:
        """Get all data needed for the home page."""
        return {
            'church_settings': self.get_church_settings(),
            'priests': self.get_priests(),
            'verse_of_day': await self.get_or_auto_create_verse_of_day(),
            'announcements': self.get_announcements(),
            'service_timings': self.get_service_timings(),
            'today_celebrations': self.get_today_celebrations(),
            'upcoming_celebrations': self.get_upcoming_celebrations(7)
        }