from typing import Optional, Dict, Any, List
from .base_repository import BaseRepository

class MemberRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "members"
    
    def get_all_members(self) -> List[Dict[str, Any]]:
        """Get all members"""
        return self.get_all(self.table_name)
    
    def get_member_by_id(self, member_id: int) -> Optional[Dict[str, Any]]:
        """Get member by ID"""
        return self.get_by_id(self.table_name, member_id)
    
    def get_member_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get member by email"""
        members = self.get_by_field(self.table_name, 'email', email)
        return members[0] if members else None
    
    def get_members_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get members by membership status"""
        return self.get_by_field(self.table_name, 'membership_status', status)
    
    def create_member(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new member"""
        return self.insert(self.table_name, member_data)
    
    def update_member(self, member_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update member"""
        return self.update(self.table_name, member_id, updates)
    
    def delete_member(self, member_id: int) -> bool:
        """Delete member"""
        return self.delete(self.table_name, member_id)
    
    def search_members(self, search_term: str) -> List[Dict[str, Any]]:
        """Search members by name or email"""
        all_members = self.get_all_members()
        search_term = search_term.lower()
        
        results = []
        for member in all_members:
            if (search_term in member.get('first_name', '').lower() or
                search_term in member.get('last_name', '').lower() or
                search_term in member.get('email', '').lower()):
                results.append(member)
        
        return results
    
    def get_members_by_ministry(self, ministry_name: str) -> List[Dict[str, Any]]:
        """Get members involved in a specific ministry"""
        all_members = self.get_all_members()
        
        results = []
        for member in all_members:
            ministry_involvement = member.get('ministry_involvement', [])
            if ministry_name in ministry_involvement:
                results.append(member)
        
        return results