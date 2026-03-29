from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
from app.services.r2_storage_service import get_r2_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/upload", tags=["File Upload"])

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """General file upload endpoint - Images only (videos not supported on R2)"""
    try:
        # Validate file type - only images allowed
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are supported")
        
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # Validate image format
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']:
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        # Read file content
        content = await file.read()
        
        # Upload to R2
        r2_service = get_r2_service()
        success, url, error = await r2_service.upload_image(
            file_content=content,
            filename=file.filename,
            folder="images",
            content_type=file.content_type
        )
        
        if not success:
            raise HTTPException(status_code=500, detail=error or "Upload failed")
        
        return {
            "success": True,
            "message": "Image uploaded successfully to R2",
            "file_url": url,
            "filename": os.path.basename(url)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/priest-image")
async def upload_priest_image(
    file: UploadFile = File(...),
    type: str = Form(...),
    name: str = Form(...)
):
    """Upload priest image to R2"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        # Read file content
        content = await file.read()
        
        # Upload to R2 in priests folder
        r2_service = get_r2_service()
        success, url, error = await r2_service.upload_image(
            file_content=content,
            filename=file.filename,
            folder="priests",
            content_type=file.content_type
        )
        
        if not success:
            raise HTTPException(status_code=500, detail=error or "Upload failed")
        
        return {
            "success": True,
            "message": "Priest image uploaded successfully to R2",
            "file_url": url,
            "filename": os.path.basename(url)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/church-logo")
async def upload_church_logo(
    file: UploadFile = File(...),
    logo_type: str = Form(...)  # 'diocese' or 'church'
):
    """Upload church or diocese logo to R2"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']:
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        # Read file content
        content = await file.read()
        
        # Upload to R2 in logos folder
        r2_service = get_r2_service()
        success, url, error = await r2_service.upload_image(
            file_content=content,
            filename=file.filename,
            folder="logos",
            content_type=file.content_type
        )
        
        if not success:
            raise HTTPException(status_code=500, detail=error or "Upload failed")
        
        return {
            "success": True,
            "message": "Logo uploaded successfully to R2",
            "file_url": url,
            "filename": os.path.basename(url)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")