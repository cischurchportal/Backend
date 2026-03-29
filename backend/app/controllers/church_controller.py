from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.church_service import ChurchService
from app.utils.responses import success_response, not_found_response, error_response

router = APIRouter(prefix="/api/church", tags=["Church"])
church_service = ChurchService()

@router.get("/home")
async def get_home_page_data():
    """Get all data needed for the home page"""
    data = church_service.get_home_page_data()
    return success_response(data=data, message="Home page data retrieved successfully")

@router.get("/settings")
async def get_church_settings():
    """Get church settings (auto-creates default if not exists)"""
    settings = church_service.get_church_settings()
    return success_response(data=settings, message="Church settings retrieved successfully")

@router.put("/settings")
async def update_church_settings(updates: dict):
    """Update church settings"""
    try:
        settings = church_service.update_church_settings(updates)
        return success_response(data=settings, message="Church settings updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.get("/priests")
async def get_priests():
    """Get all active priests"""
    priests = church_service.get_priests()
    return success_response(data={"priests": priests}, message="Priests retrieved successfully")

@router.get("/priests/{priest_id}")
async def get_priest(priest_id: int):
    """Get priest by ID"""
    priest = church_service.get_priest_by_id(priest_id)
    if not priest:
        raise not_found_response("Priest")
    
    return success_response(data=priest, message="Priest retrieved successfully")

@router.post("/priests")
async def create_priest(priest_data: dict):
    """Create a new priest"""
    try:
        priest = church_service.create_priest(priest_data)
        return success_response(data=priest, message="Priest created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/priests/{priest_id}")
async def update_priest(priest_id: int, updates: dict):
    """Update priest"""
    try:
        priest = church_service.update_priest(priest_id, updates)
        if not priest:
            raise not_found_response("Priest")
        
        return success_response(data=priest, message="Priest updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/priests/{priest_id}")
async def delete_priest(priest_id: int):
    """Delete priest"""
    success = church_service.delete_priest(priest_id)
    if not success:
        raise not_found_response("Priest")
    
    return success_response(message="Priest deleted successfully")

@router.get("/verse-of-day")
async def get_verse_of_day(date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")):
    """Get verse of the day"""
    verse = church_service.get_verse_of_day(date)
    if not verse:
        return success_response(data=None, message="No verse found for the specified date")
    
    return success_response(data=verse, message="Verse of the day retrieved successfully")

@router.post("/verse-of-day")
async def create_verse(verse_data: dict):
    """Create a new verse of the day"""
    try:
        verse = church_service.create_verse(verse_data)
        return success_response(data=verse, message="Verse created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/verse-of-day/{verse_id}")
async def update_verse(verse_id: int, updates: dict):
    """Update verse of the day"""
    try:
        verse = church_service.update_verse(verse_id, updates)
        if not verse:
            raise not_found_response("Verse")
        
        return success_response(data=verse, message="Verse updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.get("/announcements")
async def get_announcements():
    """Get active announcements"""
    announcements = church_service.get_announcements()
    return success_response(data={"announcements": announcements}, message="Announcements retrieved successfully")

@router.post("/announcements")
async def create_announcement(announcement_data: dict):
    """Create a new announcement"""
    try:
        announcement = church_service.create_announcement(announcement_data)
        return success_response(data=announcement, message="Announcement created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/announcements/{announcement_id}")
async def update_announcement(announcement_id: int, updates: dict):
    """Update announcement"""
    try:
        announcement = church_service.update_announcement(announcement_id, updates)
        if not announcement:
            raise not_found_response("Announcement")
        
        return success_response(data=announcement, message="Announcement updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/announcements/{announcement_id}")
async def delete_announcement(announcement_id: int):
    """Delete announcement"""
    success = church_service.delete_announcement(announcement_id)
    if not success:
        raise not_found_response("Announcement")
    
    return success_response(message="Announcement deleted successfully")

@router.get("/service-timings")
async def get_service_timings():
    """Get service timings"""
    services = church_service.get_service_timings()
    return success_response(data={"services": services}, message="Service timings retrieved successfully")

@router.post("/service-timings")
async def create_service_timing(service_data: dict):
    """Create a new service timing"""
    try:
        service = church_service.create_service_timing(service_data)
        return success_response(data=service, message="Service timing created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/service-timings/{service_id}")
async def update_service_timing(service_id: int, updates: dict):
    """Update service timing"""
    try:
        service = church_service.update_service_timing(service_id, updates)
        if not service:
            raise not_found_response("Service timing")
        
        return success_response(data=service, message="Service timing updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/service-timings/{service_id}")
async def delete_service_timing(service_id: int):
    """Delete service timing"""
    success = church_service.delete_service_timing(service_id)
    if not success:
        raise not_found_response("Service timing")
    
    return success_response(message="Service timing deleted successfully")

@router.get("/celebrations/today")
async def get_today_celebrations():
    """Get today's celebrations"""
    celebrations = church_service.get_today_celebrations()
    return success_response(data={"celebrations": celebrations}, message="Today's celebrations retrieved successfully")

@router.get("/celebrations/upcoming")
async def get_upcoming_celebrations(days: int = Query(7, description="Number of days to look ahead")):
    """Get upcoming celebrations"""
    celebrations = church_service.get_upcoming_celebrations(days)
    return success_response(data={"celebrations": celebrations}, message="Upcoming celebrations retrieved successfully")

@router.get("/celebrations")
async def get_all_celebrations():
    """Get all celebrations (for admin management)"""
    celebrations = church_service.get_all_celebrations()
    return success_response(data={"celebrations": celebrations}, message="All celebrations retrieved successfully")

@router.post("/celebrations")
async def create_celebration(celebration_data: dict):
    """Create a new celebration"""
    try:
        celebration = church_service.create_celebration(celebration_data)
        return success_response(data=celebration, message="Celebration created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/celebrations/{celebration_id}")
async def update_celebration(celebration_id: int, updates: dict):
    """Update celebration"""
    try:
        celebration = church_service.update_celebration(celebration_id, updates)
        if not celebration:
            raise not_found_response("Celebration")
        
        return success_response(data=celebration, message="Celebration updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/celebrations/{celebration_id}")
async def delete_celebration(celebration_id: int):
    """Delete celebration"""
    success = church_service.delete_celebration(celebration_id)
    if not success:
        raise not_found_response("Celebration")
    
    return success_response(message="Celebration deleted successfully")