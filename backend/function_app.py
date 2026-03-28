import azure.functions as func
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from azure.functions import AsgiMiddleware
from app.db.session import init_db
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

# Import configuration
try:
    from app.config import settings
    cors_origins = settings.CORS_ORIGINS
    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION
except ImportError:
    # Fallback if config not available
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
    app_name = "Church Management System API"
    app_version = "2.0.0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database (create/migrate tables) on cold start
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Database initialization failed: {e}", exc_info=True)

# Create FastAPI app
app = FastAPI(
    title=app_name,
    version=app_version,
    description="A comprehensive church management system with home page content management",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: Static blob files are no longer served from backend
# Images are now served directly from Cloudflare R2
# See R2_MIGRATION_GUIDE.md for details
logger.info("Using Cloudflare R2 for image storage")

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
    """Root endpoint with API information"""
    return {
        "message": "Church Management System API is running on Azure Functions",
        "version": app_version,
        "runtime": "Python 3.11",
        "platform": "Azure Functions",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/health",
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
    """Health check endpoint for monitoring"""
    is_azure = os.getenv("WEBSITE_INSTANCE_ID") is not None
    db_status = "unknown"
    try:
        from app.db.session import get_engine
        from sqlalchemy import text
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": app_name,
        "version": app_version,
        "runtime": "Python 3.11",
        "platform": "Azure Functions" if is_azure else "Local Development",
        "environment": "production" if is_azure else "development",
        "database": db_status
    }

# Legacy endpoint for backward compatibility
@app.post("/api/admin/login")
async def legacy_admin_login(credentials: dict):
    """Legacy admin login endpoint - redirects to new auth endpoint"""
    from app.models.schemas import LoginCredentials
    from app.controllers.auth_controller import admin_login
    
    login_creds = LoginCredentials(**credentials)
    return await admin_login(login_creds)

# Create Azure Function App
azure_app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@azure_app.function_name(name="HttpTrigger")
@azure_app.route(route="{*route}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Main Azure Function HTTP trigger that routes all requests to FastAPI"""
    logger.info(f'HTTP Request: {req.method} {req.url}')
    
    try:
        return await AsgiMiddleware(app).handle_async(req, context)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return func.HttpResponse(
            body=f'{{"error": "Internal server error", "message": "{str(e)}"}}',
            status_code=500,
            mimetype="application/json"
        )
