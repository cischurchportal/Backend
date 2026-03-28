from typing import Optional, Dict, Any, List
from app.repositories.base_repository import BaseRepository
from app.db.models import Member


class MemberRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "members"

    def get_all_members(self) -> List[Dict[str, Any]]:
        return self.get_all(self.table_name)

    def get_member_by_id(self, member_id: int) -> Optional[Dict[str, Any]]:
        return self.get_by_id(self.table_name, member_id)

    def get_member_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        results = self.get_by_field(self.table_name, "email", email)
        return results[0] if results else None

    def get_members_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self.get_by_field(self.table_name, "membership_status", status)

    def create_member(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(self.table_name, member_data)

    def update_member(self, member_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.update(self.table_name, member_id, updates)

    def delete_member(self, member_id: int) -> bool:
        return self.delete(self.table_name, member_id)

    def search_members(self, search_term: str) -> List[Dict[str, Any]]:
        all_members = self.get_all_members()
        term = search_term.lower()
        return [
            m for m in all_members
            if term in m.get("first_name", "").lower()
            or term in m.get("last_name", "").lower()
            or term in (m.get("email") or "").lower()
        ]

    def get_members_by_ministry(self, ministry_name: str) -> List[Dict[str, Any]]:
        all_members = self.get_all_members()
        return [
            m for m in all_members
            if ministry_name in (m.get("ministry_involvement") or [])
        ]
