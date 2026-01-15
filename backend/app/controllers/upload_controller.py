from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/api/upload", tags=["File Upload"])

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """General file upload endpoint"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/") and not file.content_type.startswith("video/"):
            raise HTTPException(status_code=400, detail="File must be an image or video")
        
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # Determine upload directory based on file type
        if file.content_type.startswith("image/"):
            if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                raise HTTPException(status_code=400, detail="Unsupported image format")
            upload_dir = Path("../blob/images")
        else:
            upload_dir = Path("../blob/videos")
        
        # Create directory if it doesn't exist
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = upload_dir / unique_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Return relative path for database storage
        folder = "images" if file.content_type.startswith("image/") else "videos"
        relative_path = f"/blob/{folder}/{unique_filename}"
        
        return {
            "success": True,
            "message": "File uploaded successfully",
            "file_path": relative_path,
            "filename": unique_filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/priest-image")
async def upload_priest_image(
    file: UploadFile = File(...),
    type: str = Form(...),
    name: str = Form(...)
):
    """Upload priest image"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        # Create directory if it doesn't exist
        upload_dir = Path("../blob/priests")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{file_ext}"
        file_path = upload_dir / unique_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Return relative path for database storage
        relative_path = f"/blob/priests/{unique_filename}"
        
        return {
            "success": True,
            "message": "Image uploaded successfully",
            "file_path": relative_path,
            "filename": unique_filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/church-logo")
async def upload_church_logo(
    file: UploadFile = File(...),
    logo_type: str = Form(...)  # 'diocese' or 'church'
):
    """Upload church or diocese logo"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        # Create directory if it doesn't exist
        upload_dir = Path("../blob/logos")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Use specific filename based on logo type
        filename = f"{logo_type}_logo{file_ext}"
        file_path = upload_dir / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Return relative path for database storage
        relative_path = f"/blob/logos/{filename}"
        
        return {
            "success": True,
            "message": "Logo uploaded successfully",
            "file_path": relative_path,
            "filename": filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")