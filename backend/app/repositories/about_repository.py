from datetime import datetime
from app.repositories.base_repository import BaseRepository


class AboutRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "about_page"

    def get_about_page(self):
        data = self.get_all(self.table_name)
        return data[0] if data else None

    def update_about_page(self, updates: dict):
        data = self.get_all(self.table_name)
        if not data:
            return None
        record_id = data[0]["id"]
        updates.pop("id", None)
        updates["updated_at"] = datetime.utcnow().isoformat() + "Z"
        return self.update(self.table_name, record_id, updates)
