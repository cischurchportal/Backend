from typing import Optional, Dict, Any
from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password, hash_password

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password"""
        user = self.user_repo.authenticate_user(username, password)
        
        if user:
            # Remove password from response
            user_response = user.copy()
            user_response.pop('password', None)
            return user_response
        
        return None
    
    def authenticate_admin(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate admin user"""
        user = self.authenticate_user(username, password)
        
        if user and user.get('role') == 'admin':
            return user
        
        return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user with hashed password"""
        # Hash password before storing (for now using plain text)
        # In production, use: user_data['password'] = hash_password(user_data['password'])
        
        # Check if username already exists
        existing_user = self.user_repo.get_user_by_username(user_data['username'])
        if existing_user:
            raise ValueError("Username already exists")
        
        # Check if email already exists
        existing_email = self.user_repo.get_user_by_email(user_data['email'])
        if existing_email:
            raise ValueError("Email already exists")
        
        user = self.user_repo.create_user(user_data)
        
        # Remove password from response
        user_response = user.copy()
        user_response.pop('password', None)
        return user_response
    
    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile without password"""
        user = self.user_repo.get_user_by_id(user_id)
        if user:
            user_response = user.copy()
            user_response.pop('password', None)
            return user_response
        return None
    
    def update_user_profile(self, user_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user profile"""
        # Don't allow password updates through this method
        if 'password' in updates:
            updates.pop('password')
        
        user = self.user_repo.update_user(user_id, updates)
        if user:
            user_response = user.copy()
            user_response.pop('password', None)
            return user_response
        return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return False
        
        # Verify old password
        if user.get('password') != old_password:
            return False
        
        # Update with new password (hash in production)
        # new_password_hash = hash_password(new_password)
        updated_user = self.user_repo.update_user(user_id, {'password': new_password})
        return updated_user is not None