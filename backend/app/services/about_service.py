import json
from app.repositories.about_repository import AboutRepository

class AboutService:
    def __init__(self):
        self.about_repo = AboutRepository()

    def _normalize(self, data: dict) -> dict:
        """Ensure images is always a list, not a JSON string."""
        if data and isinstance(data.get("images"), str):
            try:
                data["images"] = json.loads(data["images"])
            except (ValueError, TypeError):
                data["images"] = []
        return data

    def get_about_page(self):
        """Get the about page content"""
        return self._normalize(self.about_repo.get_about_page())

    def update_about_page(self, updates: dict):
        """Update the about page content"""
        # Ensure images is a list before saving
        if "images" in updates and isinstance(updates["images"], str):
            try:
                updates["images"] = json.loads(updates["images"])
            except (ValueError, TypeError):
                updates["images"] = []
        return self._normalize(self.about_repo.update_about_page(updates))
