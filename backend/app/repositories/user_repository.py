from typing import Optional, Dict, Any
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.db.models import User
from app.db.session import get_session_factory


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "users"

    def get_all_users(self):
        return self.get_all(self.table_name)

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.get_by_id(self.table_name, user_id)

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        results = self.get_by_field(self.table_name, "username", username)
        return results[0] if results else None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        results = self.get_by_field(self.table_name, "email", email)
        return results[0] if results else None

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(self.table_name, user_data)

    def update_user(self, user_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.update(self.table_name, user_id, updates)

    def delete_user(self, user_id: int) -> bool:
        return self.delete(self.table_name, user_id)

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.get_user_by_username(username)
        if not user or not user.get("is_active", True):
            return None
        stored_password = user.get("password", "")
        # Support both hashed (salt:hash) and legacy plain-text passwords
        from app.utils.security import verify_password
        if not verify_password(password, stored_password):
            return None
        self.update_user(user["id"], {"last_login": datetime.utcnow()})
        return user

    def get_admins(self):
        return self.get_by_field(self.table_name, "role", "admin")
