from typing import List, Optional, Dict, Any
from app.repositories.ministry_repository import MinistryRepository
from app.repositories.member_repository import MemberRepository

class MinistryService:
    def __init__(self):
        self.ministry_repo = MinistryRepository()
        self.member_repo = MemberRepository()
    
    def get_all_ministries(self) -> List[Dict[str, Any]]:
        """Get all ministries"""
        return self.ministry_repo.get_all_ministries()
    
    def get_active_ministries(self) -> List[Dict[str, Any]]:
        """Get active ministries"""
        return self.ministry_repo.get_active_ministries()
    
    def get_ministry_by_id(self, ministry_id: int) -> Optional[Dict[str, Any]]:
        """Get ministry by ID"""
        return self.ministry_repo.get_ministry_by_id(ministry_id)
    
    def create_ministry(self, ministry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new ministry"""
        # Validate leader exists
        leader_id = ministry_data.get('leader_id')
        if leader_id:
            leader = self.member_repo.get_member_by_id(leader_id)
            if not leader:
                raise ValueError("Leader not found")
        
        # Initialize empty members list
        ministry_data['members'] = []
        
        return self.ministry_repo.create_ministry(ministry_data)
    
    def update_ministry(self, ministry_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update ministry"""
        # Validate leader exists if being updated
        if 'leader_id' in updates:
            leader = self.member_repo.get_member_by_id(updates['leader_id'])
            if not leader:
                raise ValueError("Leader not found")
        
        return self.ministry_repo.update_ministry(ministry_id, updates)
    
    def delete_ministry(self, ministry_id: int) -> bool:
        """Delete ministry"""
        return self.ministry_repo.delete_ministry(ministry_id)
    
    def get_ministry_with_details(self, ministry_id: int) -> Optional[Dict[str, Any]]:
        """Get ministry with leader and member details"""
        ministry = self.ministry_repo.get_ministry_by_id(ministry_id)
        if not ministry:
            return None
        
        # Get leader details
        leader_id = ministry.get('leader_id')
        if leader_id:
            leader = self.member_repo.get_member_by_id(leader_id)
            ministry['leader_details'] = leader
        
        # Get member details
        member_ids = ministry.get('members', [])
        member_details = []
        for member_id in member_ids:
            member = self.member_repo.get_member_by_id(member_id)
            if member:
                member_details.append(member)
        ministry['member_details'] = member_details
        
        return ministry
    
    def add_member_to_ministry(self, ministry_id: int, member_id: int) -> Optional[Dict[str, Any]]:
        """Add member to ministry"""
        # Validate member exists
        member = self.member_repo.get_member_by_id(member_id)
        if not member:
            raise ValueError("Member not found")
        
        return self.ministry_repo.add_member_to_ministry(ministry_id, member_id)
    
    def remove_member_from_ministry(self, ministry_id: int, member_id: int) -> Optional[Dict[str, Any]]:
        """Remove member from ministry"""
        return self.ministry_repo.remove_member_from_ministry(ministry_id, member_id)
    
    def get_ministries_by_leader(self, leader_id: int) -> List[Dict[str, Any]]:
        """Get ministries led by a specific person"""
        return self.ministry_repo.get_ministries_by_leader(leader_id)
    
    def get_member_ministries(self, member_id: int) -> List[Dict[str, Any]]:
        """Get ministries a member belongs to"""
        all_ministries = self.ministry_repo.get_all_ministries()
        member_ministries = []
        
        for ministry in all_ministries:
            if member_id in ministry.get('members', []):
                member_ministries.append(ministry)
        
        return member_ministries
    
    def get_ministry_statistics(self) -> Dict[str, Any]:
        """Get ministry statistics"""
        all_ministries = self.ministry_repo.get_all_ministries()
        active_ministries = self.ministry_repo.get_active_ministries()
        
        stats = {
            'total_ministries': len(all_ministries),
            'active_ministries': len(active_ministries),
            'inactive_ministries': len(all_ministries) - len(active_ministries),
            'total_ministry_members': 0,
            'average_members_per_ministry': 0,
            'largest_ministry': None,
            'smallest_ministry': None
        }
        
        if active_ministries:
            member_counts = []
            largest_count = 0
            smallest_count = float('inf')
            largest_ministry = None
            smallest_ministry = None
            
            for ministry in active_ministries:
                member_count = len(ministry.get('members', []))
                member_counts.append(member_count)
                stats['total_ministry_members'] += member_count
                
                if member_count > largest_count:
                    largest_count = member_count
                    largest_ministry = ministry['name']
                
                if member_count < smallest_count:
                    smallest_count = member_count
                    smallest_ministry = ministry['name']
            
            stats['average_members_per_ministry'] = round(
                stats['total_ministry_members'] / len(active_ministries), 2
            )
            stats['largest_ministry'] = {
                'name': largest_ministry,
                'member_count': largest_count
            }
            stats['smallest_ministry'] = {
                'name': smallest_ministry,
                'member_count': smallest_count
            }
        
        return stats