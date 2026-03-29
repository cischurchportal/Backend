from fastapi import APIRouter
from app.services.about_service import AboutService
from app.utils.responses import success_response

router = APIRouter(prefix="/api/about", tags=["About"])
about_service = AboutService()

@router.get("/")
async def get_about_page():
    """Get the about page content (auto-creates default if not exists)"""
    about_data = about_service.get_about_page()
    return success_response(data=about_data, message="About page retrieved successfully")

@router.put("/")
async def update_about_page(updates: dict):
    """Update the about page content (auto-creates default if not exists)"""
    about_data = about_service.update_about_page(updates)
    return success_response(data=about_data, message="About page updated successfully")
