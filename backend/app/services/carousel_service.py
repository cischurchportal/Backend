from typing import List, Optional, Dict, Any
import os
from app.repositories.carousel_repository import CarouselRepository
from app.services.r2_storage_service import get_r2_service
import logging

logger = logging.getLogger(__name__)

class CarouselService:
    def __init__(self):
        self.carousel_repo = CarouselRepository()
    
    def get_all_carousels(self) -> List[Dict[str, Any]]:
        """Get all active carousels with their media"""
        return self.carousel_repo.get_all_carousels_with_media()
    
    def get_carousel_by_id(self, carousel_id: int) -> Optional[Dict[str, Any]]:
        """Get carousel by ID with media"""
        return self.carousel_repo.get_carousel_with_media(carousel_id)
    
    def create_carousel(self, carousel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new carousel"""
        if 'is_active' not in carousel_data:
            carousel_data['is_active'] = True
        
        if 'display_order' not in carousel_data:
            # Get the next display order
            existing_carousels = self.carousel_repo.get_active_carousels()
            max_order = max([c.get('display_order', 0) for c in existing_carousels], default=0)
            carousel_data['display_order'] = max_order + 1
        
        if 'category' not in carousel_data:
            carousel_data['category'] = 'general'
        
        return self.carousel_repo.create_carousel(carousel_data)
    
    def update_carousel(self, carousel_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update carousel"""
        return self.carousel_repo.update_carousel(carousel_id, updates)
    
    def delete_carousel(self, carousel_id: int) -> bool:
        """Delete carousel and all its media"""
        return self.carousel_repo.delete_carousel(carousel_id)
    
    def get_carousel_media(self, carousel_id: int) -> List[Dict[str, Any]]:
        """Get media for a specific carousel"""
        return self.carousel_repo.get_carousel_media(carousel_id)
    
    def add_media_to_carousel(self, carousel_id: int, media_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add media to a carousel"""
        # Validate carousel exists
        carousel = self.carousel_repo.get_carousel_by_id(carousel_id)
        if not carousel:
            raise ValueError("Carousel not found")
        
        media_data['carousel_id'] = carousel_id
        
        if 'is_active' not in media_data:
            media_data['is_active'] = True
        
        if 'display_order' not in media_data:
            # Get the next display order for this carousel
            existing_media = self.carousel_repo.get_carousel_media(carousel_id)
            max_order = max([m.get('display_order', 0) for m in existing_media], default=0)
            media_data['display_order'] = max_order + 1
        
        # Validate media type
        if media_data.get('media_type') not in ['image', 'video']:
            raise ValueError("Media type must be 'image' or 'video'")
        
        return self.carousel_repo.create_media(media_data)
    
    def update_media(self, media_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update media item"""
        return self.carousel_repo.update_media(media_id, updates)
    
    def delete_media(self, media_id: int) -> bool:
        """Delete media item"""
        return self.carousel_repo.delete_media(media_id)
    
    def reorder_carousel_media(self, carousel_id: int, media_order: List[int]) -> bool:
        """Reorder media items in a carousel"""
        # Validate all media IDs belong to the carousel
        carousel_media = self.carousel_repo.get_carousel_media(carousel_id)
        carousel_media_ids = [m['id'] for m in carousel_media]
        
        for media_id in media_order:
            if media_id not in carousel_media_ids:
                raise ValueError(f"Media ID {media_id} does not belong to carousel {carousel_id}")
        
        return self.carousel_repo.reorder_carousel_media(carousel_id, media_order)
    
    def get_carousels_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get carousels by category"""
        carousels = self.carousel_repo.get_carousels_by_category(category)
        # Add media to each carousel
        for carousel in carousels:
            carousel['media'] = self.carousel_repo.get_carousel_media(carousel['id'])
        return carousels
    
    async def upload_media_file(self, file_data: bytes, filename: str, carousel_id: int, content_type: str = "image/jpeg") -> str:
        """Upload media file to R2 storage and return file URL (images only)"""
        carousel = self.carousel_repo.get_carousel_by_id(carousel_id)
        if not carousel:
            raise ValueError("Carousel not found")

        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
            raise ValueError("Only image files are supported. Videos are not stored on R2.")

        safe_name = "".join(c for c in carousel['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_').lower()

        r2_service = get_r2_service()
        success, url, error = await r2_service.upload_image(
            file_content=file_data,
            filename=filename,
            folder=f"carousels/{safe_name}",
            content_type=content_type
        )

        if not success:
            raise Exception(error or "Failed to upload to R2")

        logger.info(f"Uploaded carousel media to R2: {url}")
        return url
    
    def get_media_statistics(self) -> Dict[str, Any]:
        """Get media statistics"""
        all_media = self.carousel_repo.get_all('carousel_media')
        active_media = [m for m in all_media if m.get('is_active', True)]
        
        stats = {
            'total_carousels': len(self.carousel_repo.get_active_carousels()),
            'total_media': len(active_media),
            'images': len([m for m in active_media if m.get('media_type') == 'image']),
            'videos': len([m for m in active_media if m.get('media_type') == 'video']),
            'media_by_category': {}
        }
        
        # Count media by carousel category
        carousels = self.carousel_repo.get_active_carousels()
        for carousel in carousels:
            category = carousel.get('category', 'general')
            if category not in stats['media_by_category']:
                stats['media_by_category'][category] = 0
            
            media_count = len(self.carousel_repo.get_carousel_media(carousel['id']))
            stats['media_by_category'][category] += media_count
        
        return stats