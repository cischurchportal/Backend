"""
One-time script to fix R2 URLs in carousel_media table.
Replaces the old private bucket URL with the correct public URL.

Run from Backend/backend/:
    python fix_r2_urls.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

OLD_PREFIX = "https://c21ee9d90c8221d1f444e2d7723e6587.r2.cloudflarestorage.com/csi-asc"
NEW_PREFIX = "https://pub-4fbcbdc1408e4124950014c8a68db319.r2.dev"

from app.db.session import get_session_factory
from app.db.models import CarouselMedia

SessionLocal = get_session_factory()

with SessionLocal() as db:
    records = db.query(CarouselMedia).filter(
        CarouselMedia.file_path.like(f"{OLD_PREFIX}%")
    ).all()

    if not records:
        print("No records to fix — all URLs already correct.")
    else:
        for r in records:
            new_url = NEW_PREFIX + r.file_path[len(OLD_PREFIX):]
            print(f"  [{r.id}] {r.file_path}\n       → {new_url}")
            r.file_path = new_url

        db.commit()
        print(f"\n✅ Fixed {len(records)} record(s).")
