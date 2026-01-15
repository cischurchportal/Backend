from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.schemas import EventCreate, EventResponse
from app.services.event_service import EventService
from app.utils.responses import success_response, not_found_response, error_response

router = APIRouter(prefix="/api/events", tags=["Events"])
event_service = EventService()

@router.get("/")
async def get_all_events():
    """Get all church events"""
    events = event_service.get_all_events()
    return success_response(data={"events": events}, message="Events retrieved successfully")

@router.get("/upcoming")
async def get_upcoming_events(limit: Optional[int] = Query(None, description="Limit number of results")):
    """Get upcoming events"""
    events = event_service.get_upcoming_events(limit)
    return success_response(data={"events": events}, message="Upcoming events retrieved successfully")

@router.get("/this-week")
async def get_events_this_week():
    """Get events for this week"""
    events = event_service.get_events_this_week()
    return success_response(data={"events": events}, message="This week's events retrieved successfully")

@router.get("/this-month")
async def get_events_this_month():
    """Get events for this month"""
    events = event_service.get_events_this_month()
    return success_response(data={"events": events}, message="This month's events retrieved successfully")

@router.get("/by-type/{event_type}")
async def get_events_by_type(event_type: str):
    """Get events by type"""
    events = event_service.get_events_by_type(event_type)
    return success_response(data={"events": events}, message=f"Events of type '{event_type}' retrieved successfully")

@router.get("/statistics")
async def get_event_statistics():
    """Get event statistics"""
    stats = event_service.get_event_statistics()
    return success_response(data=stats, message="Event statistics retrieved successfully")

@router.get("/{event_id}")
async def get_event(event_id: int):
    """Get a specific event by ID"""
    event = event_service.get_event_by_id(event_id)
    if not event:
        raise not_found_response("Event")
    
    return success_response(data=event, message="Event retrieved successfully")

@router.post("/", response_model=EventResponse)
async def create_event(event_data: EventCreate, created_by: int = Query(..., description="User ID who is creating the event")):
    """Create a new event"""
    try:
        event = event_service.create_event(event_data.dict(), created_by)
        return success_response(data=event, message="Event created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/{event_id}")
async def update_event(event_id: int, updates: dict):
    """Update event information"""
    try:
        event = event_service.update_event(event_id, updates)
        if not event:
            raise not_found_response("Event")
        
        return success_response(data=event, message="Event updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/{event_id}")
async def delete_event(event_id: int):
    """Delete an event"""
    success = event_service.delete_event(event_id)
    if not success:
        raise not_found_response("Event")
    
    return success_response(message="Event deleted successfully")

@router.post("/{event_id}/register")
async def register_for_event(event_id: int):
    """Register an attendee for an event"""
    try:
        event = event_service.register_attendee(event_id)
        if not event:
            raise not_found_response("Event")
        
        return success_response(data=event, message="Successfully registered for event")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.post("/{event_id}/unregister")
async def unregister_from_event(event_id: int):
    """Unregister an attendee from an event"""
    event = event_service.unregister_attendee(event_id)
    if not event:
        raise not_found_response("Event")
    
    return success_response(data=event, message="Successfully unregistered from event")