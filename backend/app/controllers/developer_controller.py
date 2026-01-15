from fastapi import APIRouter
from app.services.developer_service import DeveloperService
from app.utils.responses import success_response, not_found_response

router = APIRouter(prefix="/api/developers", tags=["Developers"])
developer_service = DeveloperService()

@router.get("/")
async def get_all_developers():
    """Get all developers"""
    developers = developer_service.get_all_developers()
    return success_response(data=developers, message="Developers retrieved successfully")

@router.get("/active")
async def get_active_developers():
    """Get active developers"""
    developers = developer_service.get_active_developers()
    return success_response(data=developers, message="Active developers retrieved successfully")

@router.get("/{developer_id}")
async def get_developer(developer_id: int):
    """Get a developer by ID"""
    developer = developer_service.get_developer_by_id(developer_id)
    if not developer:
        raise not_found_response("Developer")
    return success_response(data=developer, message="Developer retrieved successfully")

@router.post("/")
async def create_developer(developer_data: dict):
    """Create a new developer"""
    developer = developer_service.create_developer(developer_data)
    return success_response(data=developer, message="Developer created successfully", status_code=201)

@router.put("/{developer_id}")
async def update_developer(developer_id: int, updates: dict):
    """Update a developer"""
    developer = developer_service.update_developer(developer_id, updates)
    if not developer:
        raise not_found_response("Developer")
    return success_response(data=developer, message="Developer updated successfully")

@router.delete("/{developer_id}")
async def delete_developer(developer_id: int):
    """Delete a developer"""
    success = developer_service.delete_developer(developer_id)
    if not success:
        raise not_found_response("Developer")
    return success_response(message="Developer deleted successfully")
