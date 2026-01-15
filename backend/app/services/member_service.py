from typing import List, Optional, Dict, Any
from datetime import datetime
from app.repositories.member_repository import MemberRepository
from app.repositories.ministry_repository import MinistryRepository

class MemberService:
    def __init__(self):
        self.member_repo = MemberRepository()
        self.ministry_repo = MinistryRepository()
    
    def get_all_members(self) -> List[Dict[str, Any]]:
        """Get all members"""
        return self.member_repo.get_all_members()
    
    def get_member_by_id(self, member_id: int) -> Optional[Dict[str, Any]]:
        """Get member by ID"""
        return self.member_repo.get_member_by_id(member_id)
    
    def get_active_members(self) -> List[Dict[str, Any]]:
        """Get active members"""
        return self.member_repo.get_members_by_status('active')
    
    def create_member(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new member"""
        # Set membership date if not provided
        if 'membership_date' not in member_data:
            member_data['membership_date'] = datetime.utcnow().date().isoformat()
        
        # Validate email uniqueness
        if member_data.get('email'):
            existing_member = self.member_repo.get_member_by_email(member_data['email'])
            if existing_member:
                raise ValueError("Email already exists")
        
        return self.member_repo.create_member(member_data)
    
    def update_member(self, member_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update member"""
        # Validate email uniqueness if email is being updated
        if 'email' in updates and updates['email']:
            existing_member = self.member_repo.get_member_by_email(updates['email'])
            if existing_member and existing_member['id'] != member_id:
                raise ValueError("Email already exists")
        
        return self.member_repo.update_member(member_id, updates)
    
    def delete_member(self, member_id: int) -> bool:
        """Delete member"""
        return self.member_repo.delete_member(member_id)
    
    def search_members(self, search_term: str) -> List[Dict[str, Any]]:
        """Search members by name or email"""
        return self.member_repo.search_members(search_term)
    
    def get_member_ministries(self, member_id: int) -> List[Dict[str, Any]]:
        """Get ministries a member is involved in"""
        member = self.member_repo.get_member_by_id(member_id)
        if not member:
            return []
        
        ministry_names = member.get('ministry_involvement', [])
        ministries = []
        
        for ministry_name in ministry_names:
            # Find ministry by name
            all_ministries = self.ministry_repo.get_all_ministries()
            for ministry in all_ministries:
                if ministry.get('name').lower() == ministry_name.lower():
                    ministries.append(ministry)
                    break
        
        return ministries
    
    def add_member_to_ministry(self, member_id: int, ministry_name: str) -> bool:
        """Add member to a ministry"""
        member = self.member_repo.get_member_by_id(member_id)
        if not member:
            return False
        
        ministry_involvement = member.get('ministry_involvement', [])
        if ministry_name not in ministry_involvement:
            ministry_involvement.append(ministry_name)
            updated_member = self.member_repo.update_member(
                member_id, 
                {'ministry_involvement': ministry_involvement}
            )
            
            # Also update the ministry's member list
            all_ministries = self.ministry_repo.get_all_ministries()
            for ministry in all_ministries:
                if ministry.get('name').lower() == ministry_name.lower():
                    self.ministry_repo.add_member_to_ministry(ministry['id'], member_id)
                    break
            
            return updated_member is not None
        
        return True
    
    def remove_member_from_ministry(self, member_id: int, ministry_name: str) -> bool:
        """Remove member from a ministry"""
        member = self.member_repo.get_member_by_id(member_id)
        if not member:
            return False
        
        ministry_involvement = member.get('ministry_involvement', [])
        if ministry_name in ministry_involvement:
            ministry_involvement.remove(ministry_name)
            updated_member = self.member_repo.update_member(
                member_id, 
                {'ministry_involvement': ministry_involvement}
            )
            
            # Also update the ministry's member list
            all_ministries = self.ministry_repo.get_all_ministries()
            for ministry in all_ministries:
                if ministry.get('name').lower() == ministry_name.lower():
                    self.ministry_repo.remove_member_from_ministry(ministry['id'], member_id)
                    break
            
            return updated_member is not None
        
        return True
    
    def get_membership_statistics(self) -> Dict[str, Any]:
        """Get membership statistics"""
        all_members = self.member_repo.get_all_members()
        
        stats = {
            'total_members': len(all_members),
            'active_members': len([m for m in all_members if m.get('membership_status') == 'active']),
            'inactive_members': len([m for m in all_members if m.get('membership_status') == 'inactive']),
            'members_by_ministry': {}
        }
        
        # Count members by ministry
        for member in all_members:
            ministries = member.get('ministry_involvement', [])
            for ministry in ministries:
                if ministry not in stats['members_by_ministry']:
                    stats['members_by_ministry'][ministry] = 0
                stats['members_by_ministry'][ministry] += 1
        
        return stats