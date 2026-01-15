from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.repositories.event_repository import EventRepository

class EventService:
    def __init__(self):
        self.event_repo = EventRepository()
    
    def get_all_events(self) -> List[Dict[str, Any]]:
        """Get all events"""
        return self.event_repo.get_all_events()
    
    def get_event_by_id(self, event_id: int) -> Optional[Dict[str, Any]]:
        """Get event by ID"""
        return self.event_repo.get_event_by_id(event_id)
    
    def get_upcoming_events(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get upcoming events"""
        events = self.event_repo.get_upcoming_events()
        return events[:limit] if limit else events
    
    def get_events_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """Get events by type"""
        return self.event_repo.get_events_by_type(event_type)
    
    def create_event(self, event_data: Dict[str, Any], created_by: int) -> Dict[str, Any]:
        """Create a new event"""
        event_data['created_by'] = created_by
        event_data['current_attendees'] = 0
        
        # Validate datetime format
        try:
            datetime.fromisoformat(event_data['start_datetime'].replace('Z', '+00:00'))
            datetime.fromisoformat(event_data['end_datetime'].replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("Invalid datetime format. Use ISO format with Z suffix.")
        
        # Validate end time is after start time
        if event_data['start_datetime'] >= event_data['end_datetime']:
            raise ValueError("End time must be after start time")
        
        return self.event_repo.create_event(event_data)
    
    def update_event(self, event_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update event"""
        # Validate datetime format if provided
        for field in ['start_datetime', 'end_datetime']:
            if field in updates:
                try:
                    datetime.fromisoformat(updates[field].replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError(f"Invalid {field} format. Use ISO format with Z suffix.")
        
        # Validate end time is after start time if both are provided
        if 'start_datetime' in updates and 'end_datetime' in updates:
            if updates['start_datetime'] >= updates['end_datetime']:
                raise ValueError("End time must be after start time")
        
        return self.event_repo.update_event(event_id, updates)
    
    def delete_event(self, event_id: int) -> bool:
        """Delete event"""
        return self.event_repo.delete_event(event_id)
    
    def get_events_this_week(self) -> List[Dict[str, Any]]:
        """Get events for this week"""
        today = datetime.utcnow().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        start_date = start_of_week.isoformat()
        end_date = end_of_week.isoformat()
        
        return self.event_repo.get_events_by_date_range(start_date, end_date)
    
    def get_events_this_month(self) -> List[Dict[str, Any]]:
        """Get events for this month"""
        today = datetime.utcnow().date()
        start_of_month = today.replace(day=1)
        
        # Get last day of month
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        start_date = start_of_month.isoformat()
        end_date = end_of_month.isoformat()
        
        return self.event_repo.get_events_by_date_range(start_date, end_date)
    
    def register_attendee(self, event_id: int) -> Optional[Dict[str, Any]]:
        """Register an attendee for an event"""
        event = self.event_repo.get_event_by_id(event_id)
        if not event:
            return None
        
        current_attendees = event.get('current_attendees', 0)
        max_attendees = event.get('max_attendees')
        
        # Check if event is full
        if max_attendees and current_attendees >= max_attendees:
            raise ValueError("Event is full")
        
        return self.event_repo.update_attendee_count(event_id, current_attendees + 1)
    
    def unregister_attendee(self, event_id: int) -> Optional[Dict[str, Any]]:
        """Unregister an attendee from an event"""
        event = self.event_repo.get_event_by_id(event_id)
        if not event:
            return None
        
        current_attendees = event.get('current_attendees', 0)
        if current_attendees > 0:
            return self.event_repo.update_attendee_count(event_id, current_attendees - 1)
        
        return event
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Get event statistics"""
        all_events = self.event_repo.get_all_events()
        upcoming_events = self.event_repo.get_upcoming_events()
        recurring_events = self.event_repo.get_recurring_events()
        
        stats = {
            'total_events': len(all_events),
            'upcoming_events': len(upcoming_events),
            'recurring_events': len(recurring_events),
            'events_by_type': {},
            'total_registered_attendees': 0
        }
        
        # Count events by type and total attendees
        for event in all_events:
            event_type = event.get('event_type', 'unknown')
            if event_type not in stats['events_by_type']:
                stats['events_by_type'][event_type] = 0
            stats['events_by_type'][event_type] += 1
            
            stats['total_registered_attendees'] += event.get('current_attendees', 0)
        
        return stats