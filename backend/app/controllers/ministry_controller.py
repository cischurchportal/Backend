from fastapi import APIRouter, HTTPException
from app.models.schemas import MinistryCreate, MinistryResponse
from app.services.ministry_service import MinistryService
from app.utils.responses import success_response, not_found_response, error_response

router = APIRouter(prefix="/api/ministries", tags=["Ministries"])
ministry_service = MinistryService()

@router.get("/")
async def get_all_ministries():
    """Get all church ministries"""
    ministries = ministry_service.get_all_ministries()
    return success_response(data=ministries, message="Ministries retrieved successfully")

@router.get("/active")
async def get_active_ministries():
    """Get active ministries"""
    ministries = ministry_service.get_active_ministries()
    return success_response(data={"ministries": ministries}, message="Active ministries retrieved successfully")

@router.get("/statistics")
async def get_ministry_statistics():
    """Get ministry statistics"""
    stats = ministry_service.get_ministry_statistics()
    return success_response(data=stats, message="Ministry statistics retrieved successfully")

@router.get("/{ministry_id}")
async def get_ministry(ministry_id: int):
    """Get a specific ministry by ID"""
    ministry = ministry_service.get_ministry_by_id(ministry_id)
    if not ministry:
        raise not_found_response("Ministry")
    
    return success_response(data=ministry, message="Ministry retrieved successfully")

@router.get("/{ministry_id}/details")
async def get_ministry_with_details(ministry_id: int):
    """Get ministry with leader and member details"""
    ministry = ministry_service.get_ministry_with_details(ministry_id)
    if not ministry:
        raise not_found_response("Ministry")
    
    return success_response(data=ministry, message="Ministry details retrieved successfully")

@router.post("/", response_model=MinistryResponse)
async def create_ministry(ministry_data: MinistryCreate):
    """Create a new ministry"""
    try:
        ministry = ministry_service.create_ministry(ministry_data.dict())
        return success_response(data=ministry, message="Ministry created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/{ministry_id}")
async def update_ministry(ministry_id: int, updates: dict):
    """Update ministry information"""
    try:
        ministry = ministry_service.update_ministry(ministry_id, updates)
        if not ministry:
            raise not_found_response("Ministry")
        
        return success_response(data=ministry, message="Ministry updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/{ministry_id}")
async def delete_ministry(ministry_id: int):
    """Delete a ministry"""
    success = ministry_service.delete_ministry(ministry_id)
    if not success:
        raise not_found_response("Ministry")
    
    return success_response(message="Ministry deleted successfully")

@router.post("/{ministry_id}/members/{member_id}")
async def add_member_to_ministry(ministry_id: int, member_id: int):
    """Add a member to a ministry"""
    try:
        ministry = ministry_service.add_member_to_ministry(ministry_id, member_id)
        if not ministry:
            raise not_found_response("Ministry")
        
        return success_response(data=ministry, message="Member added to ministry successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/{ministry_id}/members/{member_id}")
async def remove_member_from_ministry(ministry_id: int, member_id: int):
    """Remove a member from a ministry"""
    ministry = ministry_service.remove_member_from_ministry(ministry_id, member_id)
    if not ministry:
        raise not_found_response("Ministry")
    
    return success_response(data=ministry, message="Member removed from ministry successfully")

@router.get("/leader/{leader_id}")
async def get_ministries_by_leader(leader_id: int):
    """Get ministries led by a specific person"""
    ministries = ministry_service.get_ministries_by_leader(leader_id)
    return success_response(data={"ministries": ministries}, message="Leader's ministries retrieved successfully")

@router.get("/member/{member_id}")
async def get_member_ministries(member_id: int):
    """Get ministries a member belongs to"""
    ministries = ministry_service.get_member_ministries(member_id)
    return success_response(data={"ministries": ministries}, message="Member's ministries retrieved successfully")