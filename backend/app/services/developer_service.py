from app.repositories.developer_repository import DeveloperRepository

class DeveloperService:
    def __init__(self):
        self.developer_repo = DeveloperRepository()
    
    def get_all_developers(self):
        """Get all developers"""
        return self.developer_repo.get_all_developers()
    
    def get_active_developers(self):
        """Get active developers"""
        return self.developer_repo.get_active_developers()
    
    def get_developer_by_id(self, developer_id: int):
        """Get a developer by ID"""
        return self.developer_repo.get_developer_by_id(developer_id)
    
    def create_developer(self, developer_data: dict):
        """Create a new developer"""
        return self.developer_repo.create_developer(developer_data)
    
    def update_developer(self, developer_id: int, updates: dict):
        """Update a developer"""
        return self.developer_repo.update_developer(developer_id, updates)
    
    def delete_developer(self, developer_id: int):
        """Delete a developer"""
        return self.developer_repo.delete_developer(developer_id)
