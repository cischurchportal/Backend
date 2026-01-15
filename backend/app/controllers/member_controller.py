from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.schemas import MemberCreate, MemberResponse
from app.services.member_service import MemberService
from app.utils.responses import success_response, not_found_response, error_response

router = APIRouter(prefix="/api/members", tags=["Members"])
member_service = MemberService()

@router.get("/")
async def get_all_members():
    """Get all church members"""
    members = member_service.get_all_members()
    return success_response(data={"members": members}, message="Members retrieved successfully")

@router.get("/active")
async def get_active_members():
    """Get active church members"""
    members = member_service.get_active_members()
    return success_response(data={"members": members}, message="Active members retrieved successfully")

@router.get("/search")
async def search_members(q: str = Query(..., description="Search term")):
    """Search members by name or email"""
    members = member_service.search_members(q)
    return success_response(data={"members": members}, message="Search results retrieved successfully")

@router.get("/statistics")
async def get_membership_statistics():
    """Get membership statistics"""
    stats = member_service.get_membership_statistics()
    return success_response(data=stats, message="Membership statistics retrieved successfully")

@router.get("/{member_id}")
async def get_member(member_id: int):
    """Get a specific member by ID"""
    member = member_service.get_member_by_id(member_id)
    if not member:
        raise not_found_response("Member")
    
    return success_response(data=member, message="Member retrieved successfully")

@router.post("/", response_model=MemberResponse)
async def create_member(member_data: MemberCreate):
    """Create a new member"""
    try:
        member = member_service.create_member(member_data.dict())
        return success_response(data=member, message="Member created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/{member_id}")
async def update_member(member_id: int, updates: dict):
    """Update member information"""
    try:
        member = member_service.update_member(member_id, updates)
        if not member:
            raise not_found_response("Member")
        
        return success_response(data=member, message="Member updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/{member_id}")
async def delete_member(member_id: int):
    """Delete a member"""
    success = member_service.delete_member(member_id)
    if not success:
        raise not_found_response("Member")
    
    return success_response(message="Member deleted successfully")

@router.get("/{member_id}/ministries")
async def get_member_ministries(member_id: int):
    """Get ministries a member is involved in"""
    ministries = member_service.get_member_ministries(member_id)
    return success_response(data={"ministries": ministries}, message="Member ministries retrieved successfully")

@router.post("/{member_id}/ministries/{ministry_name}")
async def add_member_to_ministry(member_id: int, ministry_name: str):
    """Add member to a ministry"""
    success = member_service.add_member_to_ministry(member_id, ministry_name)
    if not success:
        raise error_response("Failed to add member to ministry")
    
    return success_response(message="Member added to ministry successfully")

@router.delete("/{member_id}/ministries/{ministry_name}")
async def remove_member_from_ministry(member_id: int, ministry_name: str):
    """Remove member from a ministry"""
    success = member_service.remove_member_from_ministry(member_id, ministry_name)
    if not success:
        raise error_response("Failed to remove member from ministry")
    
    return success_response(message="Member removed from ministry successfully")