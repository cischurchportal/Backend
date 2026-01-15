from app.repositories.base_repository import BaseRepository

class AboutRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = 'about_page'
    
    def get_about_page(self):
        """Get the about page content"""
        data = self._load_table(self.table_name)
        return data[0] if data else None
    
    def update_about_page(self, updates: dict):
        """Update the about page content"""
        data = self._load_table(self.table_name)
        if not data:
            return None
        
        # Update the first (and only) record
        for key, value in updates.items():
            if key != 'id':
                data[0][key] = value
        
        from datetime import datetime
        data[0]['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        self._save_table(self.table_name, data)
        return data[0]
