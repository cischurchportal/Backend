from fastapi import APIRouter
from app.services.about_service import AboutService
from app.utils.responses import success_response, not_found_response

router = APIRouter(prefix="/api/about", tags=["About"])
about_service = AboutService()

@router.get("/")
async def get_about_page():
    """Get the about page content"""
    about_data = about_service.get_about_page()
    if not about_data:
        raise not_found_response("About page")
    
    return success_response(data=about_data, message="About page retrieved successfully")

@router.put("/")
async def update_about_page(updates: dict):
    """Update the about page content"""
    about_data = about_service.update_about_page(updates)
    if not about_data:
        raise not_found_response("About page")
    
    return success_response(data=about_data, message="About page updated successfully")
