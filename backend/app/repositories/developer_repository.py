from app.repositories.base_repository import BaseRepository

class DeveloperRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = 'developers'
    
    def get_all_developers(self):
        """Get all developers"""
        return self._load_table(self.table_name)
    
    def get_active_developers(self):
        """Get active developers ordered by order field"""
        developers = self._load_table(self.table_name)
        active = [d for d in developers if d.get('is_active', True)]
        return sorted(active, key=lambda x: x.get('order', 999))
    
    def get_developer_by_id(self, developer_id: int):
        """Get a developer by ID"""
        return self.get_by_id(self.table_name, developer_id)
    
    def create_developer(self, developer_data: dict):
        """Create a new developer"""
        return self.insert(self.table_name, developer_data)
    
    def update_developer(self, developer_id: int, updates: dict):
        """Update a developer"""
        return self.update(self.table_name, developer_id, updates)
    
    def delete_developer(self, developer_id: int):
        """Delete a developer"""
        return self.delete(self.table_name, developer_id)
