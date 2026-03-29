from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from app.services.carousel_service import CarouselService
from app.utils.responses import success_response, not_found_response, error_response

router = APIRouter(prefix="/api/carousels", tags=["Carousels"])
carousel_service = CarouselService()

@router.get("/")
async def get_all_carousels():
    """Get all active carousels with their media"""
    carousels = carousel_service.get_all_carousels()
    return success_response(data={"carousels": carousels}, message="Carousels retrieved successfully")

@router.get("/statistics")
async def get_media_statistics():
    """Get media statistics"""
    stats = carousel_service.get_media_statistics()
    return success_response(data=stats, message="Media statistics retrieved successfully")

@router.get("/category/{category}")
async def get_carousels_by_category(category: str):
    """Get carousels by category"""
    carousels = carousel_service.get_carousels_by_category(category)
    return success_response(data={"carousels": carousels}, message=f"Carousels in category '{category}' retrieved successfully")

@router.get("/{carousel_id}")
async def get_carousel(carousel_id: int):
    """Get carousel by ID with media"""
    carousel = carousel_service.get_carousel_by_id(carousel_id)
    if not carousel:
        raise not_found_response("Carousel")
    
    return success_response(data=carousel, message="Carousel retrieved successfully")

@router.post("/")
async def create_carousel(carousel_data: dict):
    """Create a new carousel"""
    try:
        carousel = carousel_service.create_carousel(carousel_data)
        return success_response(data=carousel, message="Carousel created successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.put("/{carousel_id}")
async def update_carousel(carousel_id: int, updates: dict):
    """Update carousel"""
    try:
        carousel = carousel_service.update_carousel(carousel_id, updates)
        if not carousel:
            raise not_found_response("Carousel")
        
        return success_response(data=carousel, message="Carousel updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/{carousel_id}")
async def delete_carousel(carousel_id: int):
    """Delete carousel and all its media"""
    success = carousel_service.delete_carousel(carousel_id)
    if not success:
        raise not_found_response("Carousel")
    
    return success_response(message="Carousel deleted successfully")

@router.get("/{carousel_id}/media")
async def get_carousel_media(carousel_id: int):
    """Get media for a specific carousel"""
    media = carousel_service.get_carousel_media(carousel_id)
    return success_response(data={"media": media}, message="Carousel media retrieved successfully")

@router.post("/{carousel_id}/media")
async def add_media_to_carousel(carousel_id: int, media_data: dict):
    """Add media to a carousel"""
    try:
        media = carousel_service.add_media_to_carousel(carousel_id, media_data)
        return success_response(data=media, message="Media added to carousel successfully", status_code=201)
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.post("/{carousel_id}/upload")
async def upload_media_file(
    carousel_id: int,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    media_type: str = Form(...)
):
    """Upload image file to carousel (images only - use /video endpoint for videos)"""
    try:
        if media_type != "image":
            raise ValueError("Only image files are supported via upload. Use the /video endpoint for YouTube videos.")
        
        if not file.content_type.startswith("image/"):
            raise ValueError("Invalid image file type")
        
        file_data = await file.read()
        
        file_url = await carousel_service.upload_media_file(
            file_data, 
            file.filename, 
            carousel_id,
            content_type=file.content_type
        )
        
        media_data = {
            "media_type": "image",
            "file_path": file_url,
            "title": title,
            "description": description or ""
        }
        
        media = carousel_service.add_media_to_carousel(carousel_id, media_data)
        return success_response(data=media, message="Image uploaded successfully", status_code=201)
        
    except ValueError as e:
        raise error_response(str(e), status_code=400)
    except Exception as e:
        raise error_response(f"Failed to upload media: {str(e)}", status_code=500)

@router.post("/{carousel_id}/video")
async def add_youtube_video(carousel_id: int, video_data: dict):
    """Add a YouTube video to a carousel by providing a YouTube URL"""
    import re
    try:
        youtube_url = video_data.get("youtube_url", "").strip()
        title = video_data.get("title", "").strip()
        description = video_data.get("description", "")

        if not title:
            raise ValueError("Title is required")

        # Extract YouTube video ID from various URL formats
        patterns = [
            r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})",
        ]
        video_id = None
        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                video_id = match.group(1)
                break

        if not video_id:
            raise ValueError("Invalid YouTube URL. Please provide a valid YouTube video link.")

        # Store the canonical embed URL
        embed_url = f"https://www.youtube.com/embed/{video_id}"

        media_data = {
            "media_type": "video",
            "file_path": embed_url,
            "title": title,
            "description": description or ""
        }

        media = carousel_service.add_media_to_carousel(carousel_id, media_data)
        return success_response(data=media, message="YouTube video added successfully", status_code=201)

    except ValueError as e:
        raise error_response(str(e), status_code=400)
    except Exception as e:
        raise error_response(f"Failed to add video: {str(e)}", status_code=500)

@router.put("/media/{media_id}")
async def update_media(media_id: int, updates: dict):
    """Update media item"""
    try:
        media = carousel_service.update_media(media_id, updates)
        if not media:
            raise not_found_response("Media")
        
        return success_response(data=media, message="Media updated successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)

@router.delete("/media/{media_id}")
async def delete_media(media_id: int):
    """Delete media item"""
    success = carousel_service.delete_media(media_id)
    if not success:
        raise not_found_response("Media")
    
    return success_response(message="Media deleted successfully")

@router.put("/{carousel_id}/media/reorder")
async def reorder_carousel_media(carousel_id: int, media_order: dict):
    """Reorder media items in a carousel"""
    try:
        # Extract media order from request body
        order_list = media_order.get("order", [])
        if not order_list:
            raise ValueError("Media order list is required")
        
        success = carousel_service.reorder_carousel_media(carousel_id, order_list)
        if not success:
            raise error_response("Failed to reorder media")
        
        return success_response(message="Media reordered successfully")
    except ValueError as e:
        raise error_response(str(e), status_code=400)