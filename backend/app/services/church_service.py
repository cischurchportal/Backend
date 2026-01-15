from typing import List, Optional, Dict, Any
from datetime import datetime, date
from app.repositories.church_repository import ChurchRepository

class ChurchService:
    def __init__(self):
        self.church_repo = ChurchRepository()
    
    def get_church_settings(self) -> Optional[Dict[str, Any]]:
        """Get church settings"""
        return self.church_repo.get_church_settings()
    
    def update_church_settings(self, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update church settings"""
        return self.church_repo.update_church_settings(updates)
    
    def get_priests(self) -> List[Dict[str, Any]]:
        """Get all active priests"""
        return self.church_repo.get_priests()
    
    def get_priest_by_id(self, priest_id: int) -> Optional[Dict[str, Any]]:
        """Get priest by ID"""
        return self.church_repo.get_priest_by_id(priest_id)
    
    def create_priest(self, priest_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new priest"""
        # Set default values
        if 'is_active' not in priest_data:
            priest_data['is_active'] = True
        
        if 'display_order' not in priest_data:
            # Get the next display order
            existing_priests = self.church_repo.get_priests()
            max_order = max([p.get('display_order', 0) for p in existing_priests], default=0)
            priest_data['display_order'] = max_order + 1
        
        return self.church_repo.create_priest(priest_data)
    
    def update_priest(self, priest_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update priest"""
        return self.church_repo.update_priest(priest_id, updates)
    
    def delete_priest(self, priest_id: int) -> bool:
        """Delete priest"""
        return self.church_repo.delete_priest(priest_id)
    
    def get_verse_of_day(self, date_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get verse of the day for a specific date or today"""
        if not date_str:
            date_str = date.today().isoformat()
        
        verse = self.church_repo.get_verse_of_day(date_str)
        if not verse:
            # If no verse for today, get the latest verse
            verse = self.church_repo.get_latest_verse()
        
        return verse
    
    def create_verse(self, verse_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new verse of the day"""
        if 'is_active' not in verse_data:
            verse_data['is_active'] = True
        
        if 'date' not in verse_data:
            verse_data['date'] = date.today().isoformat()
        
        return self.church_repo.create_verse(verse_data)
    
    def update_verse(self, verse_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update verse of the day"""
        return self.church_repo.update_verse(verse_id, updates)
    
    def get_announcements(self) -> List[Dict[str, Any]]:
        """Get active announcements"""
        return self.church_repo.get_active_announcements()
    
    def create_announcement(self, announcement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new announcement"""
        if 'is_active' not in announcement_data:
            announcement_data['is_active'] = True
        
        if 'priority' not in announcement_data:
            announcement_data['priority'] = 'medium'
        
        if 'type' not in announcement_data:
            announcement_data['type'] = 'general'
        
        return self.church_repo.create_announcement(announcement_data)
    
    def update_announcement(self, announcement_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update announcement"""
        return self.church_repo.update_announcement(announcement_id, updates)
    
    def delete_announcement(self, announcement_id: int) -> bool:
        """Delete announcement"""
        return self.church_repo.delete_announcement(announcement_id)
    
    def get_service_timings(self) -> List[Dict[str, Any]]:
        """Get service timings"""
        return self.church_repo.get_service_timings()
    
    def create_service_timing(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new service timing"""
        if 'is_active' not in service_data:
            service_data['is_active'] = True
        
        if 'language' not in service_data:
            service_data['language'] = 'English'
        
        return self.church_repo.create_service_timing(service_data)
    
    def update_service_timing(self, service_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update service timing"""
        return self.church_repo.update_service_timing(service_id, updates)
    
    def delete_service_timing(self, service_id: int) -> bool:
        """Delete service timing"""
        return self.church_repo.delete_service_timing(service_id)
    
    def get_today_celebrations(self) -> List[Dict[str, Any]]:
        """Get today's celebrations"""
        today = date.today().isoformat()
        return self.church_repo.get_today_celebrations(today)
    
    def get_upcoming_celebrations(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get upcoming celebrations"""
        return self.church_repo.get_upcoming_celebrations(days)
    
    def create_celebration(self, celebration_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new celebration"""
        if 'is_active' not in celebration_data:
            celebration_data['is_active'] = True
        
        if 'date' not in celebration_data:
            celebration_data['date'] = date.today().isoformat()
        
        return self.church_repo.create_celebration(celebration_data)
    
    def update_celebration(self, celebration_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update celebration"""
        return self.church_repo.update_celebration(celebration_id, updates)
    
    def delete_celebration(self, celebration_id: int) -> bool:
        """Delete celebration"""
        return self.church_repo.delete_celebration(celebration_id)
    
    def get_home_page_data(self) -> Dict[str, Any]:
        """Get all data needed for the home page"""
        return {
            'church_settings': self.get_church_settings(),
            'priests': self.get_priests(),
            'verse_of_day': self.get_verse_of_day(),
            'announcements': self.get_announcements(),
            'service_timings': self.get_service_timings(),
            'today_celebrations': self.get_today_celebrations(),
            'upcoming_celebrations': self.get_upcoming_celebrations(7)
        }