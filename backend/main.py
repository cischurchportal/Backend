from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.controllers import auth_controller
from app.controllers import member_controller
from app.controllers import event_controller
from app.controllers import ministry_controller
from app.controllers import donation_controller
from app.controllers import church_controller
from app.controllers import carousel_controller
from app.controllers import upload_controller
from app.controllers import about_controller
from app.controllers import developer_controller

# Create FastAPI app
app = FastAPI(
    title="Church Management System API",
    version="2.0.0",
    description="A comprehensive church management system with home page content management"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from blob directory
app.mount("/blob", StaticFiles(directory="../blob"), name="blob")

# Include routers
app.include_router(auth_controller.router)
app.include_router(church_controller.router)
app.include_router(about_controller.router)
app.include_router(carousel_controller.router)
app.include_router(upload_controller.router)
app.include_router(member_controller.router)
app.include_router(event_controller.router)
app.include_router(ministry_controller.router)
app.include_router(donation_controller.router)
app.include_router(developer_controller.router)

@app.get("/")
async def root():
    return {
        "message": "Church Management System API is running",
        "version": "2.0.0",
        "docs": "/docs",
        "features": [
            "Church home page management",
            "Priest management",
            "Verse of the day",
            "Announcements",
            "Service timings",
            "Celebrations tracking",
            "Carousel management",
            "Member management",
            "Event management",
            "Ministry management",
            "Donation tracking"
        ]
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Church Management System API",
        "version": "2.0.0"
    }

# Legacy endpoint for backward compatibility
@app.post("/api/admin/login")
async def legacy_admin_login(credentials: dict):
    """Legacy admin login endpoint - redirects to new auth endpoint"""
    from app.models.schemas import LoginCredentials
    from app.controllers.auth_controller import admin_login
    
    login_creds = LoginCredentials(**credentials)
    return await admin_login(login_creds)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)