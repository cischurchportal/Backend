from app.repositories.base_repository import BaseRepository


class AboutRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "about_page"

    def _ensure_record(self):
        """Return existing record or create a default one."""
        data = self.get_all(self.table_name)
        if data:
            return data[0]
        # Seed a default record — let the DB model handle updated_at default
        default = {
            "title": "About Our Church",
            "history": "",
            "images": []
        }
        return self.insert(self.table_name, default)

    def get_about_page(self):
        return self._ensure_record()

    def update_about_page(self, updates: dict):
        record = self._ensure_record()
        record_id = record["id"]
        updates.pop("id", None)
        updates.pop("updated_at", None)  # let base_repository handle this
        return self.update(self.table_name, record_id, updates)
