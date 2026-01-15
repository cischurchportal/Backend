from typing import Optional, Dict, Any, List
from .base_repository import BaseRepository

class ChurchRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def get_church_settings(self) -> Optional[Dict[str, Any]]:
        """Get church settings"""
        settings = self.get_all('church_settings')
        return settings[0] if settings else None
    
    def update_church_settings(self, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update church settings"""
        settings = self.get_church_settings()
        if settings:
            return self.update('church_settings', settings['id'], updates)
        return None
    
    def get_priests(self) -> List[Dict[str, Any]]:
        """Get all active priests ordered by display_order"""
        priests = self.get_by_field('priests', 'is_active', True)
        return sorted(priests, key=lambda x: x.get('display_order', 999))
    
    def get_priest_by_id(self, priest_id: int) -> Optional[Dict[str, Any]]:
        """Get priest by ID"""
        return self.get_by_id('priests', priest_id)
    
    def create_priest(self, priest_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new priest"""
        return self.insert('priests', priest_data)
    
    def update_priest(self, priest_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update priest"""
        return self.update('priests', priest_id, updates)
    
    def delete_priest(self, priest_id: int) -> bool:
        """Delete priest"""
        return self.delete('priests', priest_id)
    
    def get_verse_of_day(self, date: str) -> Optional[Dict[str, Any]]:
        """Get verse of the day for a specific date"""
        verses = self.get_by_field('verse_of_day', 'date', date)
        active_verses = [v for v in verses if v.get('is_active', True)]
        return active_verses[0] if active_verses else None
    
    def get_latest_verse(self) -> Optional[Dict[str, Any]]:
        """Get the latest active verse"""
        verses = self.get_by_field('verse_of_day', 'is_active', True)
        if verses:
            return max(verses, key=lambda x: x.get('date', ''))
        return None
    
    def create_verse(self, verse_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new verse of the day"""
        return self.insert('verse_of_day', verse_data)
    
    def update_verse(self, verse_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update verse of the day"""
        return self.update('verse_of_day', verse_id, updates)
    
    def get_active_announcements(self) -> List[Dict[str, Any]]:
        """Get active announcements ordered by priority"""
        announcements = self.get_by_field('announcements', 'is_active', True)
        # Sort by priority (high, medium, low) then by creation date
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        return sorted(announcements, key=lambda x: (
            priority_order.get(x.get('priority', 'low'), 3),
            x.get('created_at', '')
        ))
    
    def create_announcement(self, announcement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new announcement"""
        return self.insert('announcements', announcement_data)
    
    def update_announcement(self, announcement_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update announcement"""
        return self.update('announcements', announcement_id, updates)
    
    def delete_announcement(self, announcement_id: int) -> bool:
        """Delete announcement"""
        return self.delete('announcements', announcement_id)
    
    def get_service_timings(self) -> List[Dict[str, Any]]:
        """Get active service timings"""
        services = self.get_by_field('service_timings', 'is_active', True)
        # Sort by day of week and time
        day_order = {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 
                    'Thursday': 5, 'Friday': 6, 'Saturday': 7}
        return sorted(services, key=lambda x: (
            day_order.get(x.get('day_of_week', 'Sunday'), 1),
            x.get('time', '00:00')
        ))
    
    def create_service_timing(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new service timing"""
        return self.insert('service_timings', service_data)
    
    def update_service_timing(self, service_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update service timing"""
        return self.update('service_timings', service_id, updates)
    
    def delete_service_timing(self, service_id: int) -> bool:
        """Delete service timing"""
        return self.delete('service_timings', service_id)
    
    def get_today_celebrations(self, date: str) -> List[Dict[str, Any]]:
        """Get celebrations for today"""
        celebrations = self.get_by_field('celebrations', 'date', date)
        return [c for c in celebrations if c.get('is_active', True)]
    
    def get_upcoming_celebrations(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get upcoming celebrations within specified days"""
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        
        all_celebrations = self.get_by_field('celebrations', 'is_active', True)
        upcoming = []
        
        for celebration in all_celebrations:
            celebration_date = datetime.strptime(celebration.get('date', ''), '%Y-%m-%d').date()
            if today <= celebration_date <= end_date:
                upcoming.append(celebration)
        
        return sorted(upcoming, key=lambda x: x.get('date', ''))
    
    def create_celebration(self, celebration_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new celebration"""
        return self.insert('celebrations', celebration_data)
    
    def update_celebration(self, celebration_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update celebration"""
        return self.update('celebrations', celebration_id, updates)
    
    def delete_celebration(self, celebration_id: int) -> bool:
        """Delete celebration"""
        return self.delete('celebrations', celebration_id)