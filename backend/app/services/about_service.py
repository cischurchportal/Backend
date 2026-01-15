from app.repositories.about_repository import AboutRepository

class AboutService:
    def __init__(self):
        self.about_repo = AboutRepository()
    
    def get_about_page(self):
        """Get the about page content"""
        return self.about_repo.get_about_page()
    
    def update_about_page(self, updates: dict):
        """Update the about page content"""
        return self.about_repo.update_about_page(updates)
