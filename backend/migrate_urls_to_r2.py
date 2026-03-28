"""
Script to migrate database JSON files from local blob paths to R2 URLs
Run this after uploading existing images to R2
"""
import json
import os
from pathlib import Path

# R2 base URL
R2_BASE_URL = "https://c21ee9d90c8221d1f444e2d7723e6587.r2.cloudflarestorage.com/csi-asc"

def migrate_url(old_path: str) -> str:
    """Convert local blob path to R2 URL"""
    if not old_path:
        return old_path
    
    # If already an R2 URL, return as is
    if old_path.startswith("https://"):
        return old_path
    
    # Remove leading /blob/ if present
    if old_path.startswith("/blob/"):
        old_path = old_path[6:]  # Remove "/blob/"
    elif old_path.startswith("blob/"):
        old_path = old_path[5:]  # Remove "blob/"
    
    # Construct R2 URL
    return f"{R2_BASE_URL}/{old_path}"

def migrate_json_file(file_path: str, fields_to_migrate: list):
    """Migrate a JSON file's image fields to R2 URLs"""
    print(f"\nProcessing: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"  ⚠️  File not found, skipping")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            data = [data]
        
        updated_count = 0
        for item in data:
            for field in fields_to_migrate:
                if field in item and item[field]:
                    old_value = item[field]
                    new_value = migrate_url(old_value)
                    if old_value != new_value:
                        item[field] = new_value
                        updated_count += 1
                        print(f"  ✓ Updated {field}: {old_value} -> {new_value}")
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Updated {updated_count} field(s)")
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

def main():
    """Main migration function"""
    print("=" * 60)
    print("Database URL Migration: Local Blob -> Cloudflare R2")
    print("=" * 60)
    
    database_path = Path("../database")
    
    # Define files and their image fields
    migrations = [
        {
            "file": database_path / "church_settings.json",
            "fields": ["diocese_logo", "church_logo"]
        },
        {
            "file": database_path / "developers.json",
            "fields": ["image"]
        },
        {
            "file": database_path / "carousel_media.json",
            "fields": ["file_path"]
        },
        {
            "file": database_path / "ministries.json",
            "fields": ["image"]
        },
        {
            "file": database_path / "priests.json",
            "fields": ["image"]
        },
        {
            "file": database_path / "about_page.json",
            "fields": ["image", "logo"]
        },
        {
            "file": database_path / "events.json",
            "fields": ["image"]
        },
        {
            "file": database_path / "members.json",
            "fields": ["photo"]
        }
    ]
    
    # Process each file
    for migration in migrations:
        migrate_json_file(str(migration["file"]), migration["fields"])
    
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the updated JSON files")
    print("2. Upload existing images from blob/ folder to R2")
    print("3. Test the application with new R2 URLs")
    print("4. Update frontend to use full R2 URLs")

if __name__ == "__main__":
    main()
