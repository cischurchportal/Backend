from typing import Optional, Dict, Any, List
from .base_repository import BaseRepository

class CarouselRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def get_active_carousels(self) -> List[Dict[str, Any]]:
        """Get all active carousels ordered by display_order"""
        carousels = self.get_by_field('carousels', 'is_active', True)
        return sorted(carousels, key=lambda x: x.get('display_order', 999))
    
    def get_carousel_by_id(self, carousel_id: int) -> Optional[Dict[str, Any]]:
        """Get carousel by ID"""
        return self.get_by_id('carousels', carousel_id)
    
    def create_carousel(self, carousel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new carousel"""
        return self.insert('carousels', carousel_data)
    
    def update_carousel(self, carousel_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update carousel"""
        return self.update('carousels', carousel_id, updates)
    
    def delete_carousel(self, carousel_id: int) -> bool:
        """Delete carousel"""
        # First delete all media in this carousel
        media_items = self.get_carousel_media(carousel_id)
        for media in media_items:
            self.delete('carousel_media', media['id'])
        
        # Then delete the carousel
        return self.delete('carousels', carousel_id)
    
    def get_carousel_media(self, carousel_id: int) -> List[Dict[str, Any]]:
        """Get all active media for a carousel ordered by display_order"""
        media = self.get_by_field('carousel_media', 'carousel_id', carousel_id)
        active_media = [m for m in media if m.get('is_active', True)]
        return sorted(active_media, key=lambda x: x.get('display_order', 999))
    
    def get_media_by_id(self, media_id: int) -> Optional[Dict[str, Any]]:
        """Get media by ID"""
        return self.get_by_id('carousel_media', media_id)
    
    def create_media(self, media_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new media item"""
        return self.insert('carousel_media', media_data)
    
    def update_media(self, media_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update media item"""
        return self.update('carousel_media', media_id, updates)
    
    def delete_media(self, media_id: int) -> bool:
        """Delete media item"""
        return self.delete('carousel_media', media_id)
    
    def get_carousel_with_media(self, carousel_id: int) -> Optional[Dict[str, Any]]:
        """Get carousel with its media items"""
        carousel = self.get_carousel_by_id(carousel_id)
        if carousel:
            carousel['media'] = self.get_carousel_media(carousel_id)
        return carousel
    
    def get_all_carousels_with_media(self) -> List[Dict[str, Any]]:
        """Get all active carousels with their media"""
        carousels = self.get_active_carousels()
        for carousel in carousels:
            carousel['media'] = self.get_carousel_media(carousel['id'])
        return carousels
    
    def get_carousels_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get carousels by category"""
        all_carousels = self.get_active_carousels()
        return [c for c in all_carousels if c.get('category', '').lower() == category.lower()]
    
    def reorder_carousel_media(self, carousel_id: int, media_order: List[int]) -> bool:
        """Reorder media items in a carousel"""
        try:
            for index, media_id in enumerate(media_order):
                self.update_media(media_id, {'display_order': index + 1})
            return True
        except Exception:
            return False
    
    def get_media_by_type(self, media_type: str) -> List[Dict[str, Any]]:
        """Get media by type (image/video)"""
        all_media = self.get_all('carousel_media')
        return [m for m in all_media if m.get('media_type', '').lower() == media_type.lower() and m.get('is_active', True)]