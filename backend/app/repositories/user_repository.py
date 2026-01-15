from typing import Optional, Dict, Any
from datetime import datetime
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "users"
    
    def get_all_users(self):
        """Get all users"""
        return self.get_all(self.table_name)
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.get_by_id(self.table_name, user_id)
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        users = self.get_by_field(self.table_name, 'username', username)
        return users[0] if users else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        users = self.get_by_field(self.table_name, 'email', email)
        return users[0] if users else None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        return self.insert(self.table_name, user_data)
    
    def update_user(self, user_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user"""
        return self.update(self.table_name, user_id, updates)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        return self.delete(self.table_name, user_id)
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user"""
        user = self.get_user_by_username(username)
        
        if user and user.get('password') == password and user.get('is_active', True):
            # Update last login
            self.update_user(user['id'], {'last_login': datetime.utcnow().isoformat() + 'Z'})
            return user
        
        return None
    
    def get_admins(self):
        """Get all admin users"""
        return self.get_by_field(self.table_name, 'role', 'admin')