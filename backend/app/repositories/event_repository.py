from typing import Optional, Dict, Any, List
from datetime import datetime
from .base_repository import BaseRepository

class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name = "events"
    
    def get_all_events(self) -> List[Dict[str, Any]]:
        """Get all events"""
        return self.get_all(self.table_name)
    
    def get_event_by_id(self, event_id: int) -> Optional[Dict[str, Any]]:
        """Get event by ID"""
        return self.get_by_id(self.table_name, event_id)
    
    def get_events_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """Get events by type"""
        return self.get_by_field(self.table_name, 'event_type', event_type)
    
    def get_upcoming_events(self) -> List[Dict[str, Any]]:
        """Get upcoming events"""
        all_events = self.get_all_events()
        current_time = datetime.utcnow().isoformat() + 'Z'
        
        upcoming = []
        for event in all_events:
            if event.get('start_datetime', '') > current_time:
                upcoming.append(event)
        
        # Sort by start datetime
        upcoming.sort(key=lambda x: x.get('start_datetime', ''))
        return upcoming
    
    def get_recurring_events(self) -> List[Dict[str, Any]]:
        """Get recurring events"""
        return self.get_by_field(self.table_name, 'is_recurring', True)
    
    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new event"""
        return self.insert(self.table_name, event_data)
    
    def update_event(self, event_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update event"""
        return self.update(self.table_name, event_id, updates)
    
    def delete_event(self, event_id: int) -> bool:
        """Delete event"""
        return self.delete(self.table_name, event_id)
    
    def get_events_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get events within a date range"""
        all_events = self.get_all_events()
        
        results = []
        for event in all_events:
            event_start = event.get('start_datetime', '')
            if start_date <= event_start <= end_date:
                results.append(event)
        
        return results
    
    def update_attendee_count(self, event_id: int, count: int) -> Optional[Dict[str, Any]]:
        """Update current attendee count"""
        return self.update_event(event_id, {'current_attendees': count})