from typing import Optional, Dict, Any, List
from .base_repository import BaseRepository

class MinistryRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "ministries"
    
    def get_all_ministries(self) -> List[Dict[str, Any]]:
        """Get all ministries"""
        return self.get_all(self.table_name)
    
    def get_ministry_by_id(self, ministry_id: int) -> Optional[Dict[str, Any]]:
        """Get ministry by ID"""
        return self.get_by_id(self.table_name, ministry_id)
    
    def get_active_ministries(self) -> List[Dict[str, Any]]:
        """Get active ministries"""
        return self.get_by_field(self.table_name, 'is_active', True)
    
    def get_ministries_by_leader(self, leader_id: int) -> List[Dict[str, Any]]:
        """Get ministries led by a specific person"""
        return self.get_by_field(self.table_name, 'leader_id', leader_id)
    
    def create_ministry(self, ministry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new ministry"""
        return self.insert(self.table_name, ministry_data)
    
    def update_ministry(self, ministry_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update ministry"""
        return self.update(self.table_name, ministry_id, updates)
    
    def delete_ministry(self, ministry_id: int) -> bool:
        """Delete ministry"""
        return self.delete(self.table_name, ministry_id)
    
    def add_member_to_ministry(self, ministry_id: int, member_id: int) -> Optional[Dict[str, Any]]:
        """Add a member to a ministry"""
        ministry = self.get_ministry_by_id(ministry_id)
        if ministry:
            members = ministry.get('members', [])
            if member_id not in members:
                members.append(member_id)
                return self.update_ministry(ministry_id, {'members': members})
        return None
    
    def remove_member_from_ministry(self, ministry_id: int, member_id: int) -> Optional[Dict[str, Any]]:
        """Remove a member from a ministry"""
        ministry = self.get_ministry_by_id(ministry_id)
        if ministry:
            members = ministry.get('members', [])
            if member_id in members:
                members.remove(member_id)
                return self.update_ministry(ministry_id, {'members': members})
        return None
    
    def get_ministry_members(self, ministry_id: int) -> List[int]:
        """Get member IDs for a ministry"""
        ministry = self.get_ministry_by_id(ministry_id)
        return ministry.get('members', []) if ministry else []