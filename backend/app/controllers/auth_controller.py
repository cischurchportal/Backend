from fastapi import APIRouter, HTTPException
from app.models.schemas import LoginCredentials, LoginResponse
from app.services.auth_service import AuthService
from app.utils.responses import success_response, unauthorized_response

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginCredentials):
    """User login endpoint"""
    user = auth_service.authenticate_user(credentials.username, credentials.password)
    
    if user:
        return LoginResponse(
            message="Login successful!",
            success=True,
            user=user
        )
    else:
        raise unauthorized_response("Invalid username or password")

@router.post("/admin/login", response_model=LoginResponse)
async def admin_login(credentials: LoginCredentials):
    """Admin login endpoint"""
    user = auth_service.authenticate_admin(credentials.username, credentials.password)
    
    if user:
        return LoginResponse(
            message="Login successful! Welcome to the admin panel.",
            success=True,
            user=user
        )
    else:
        raise unauthorized_response("Invalid admin credentials")

@router.get("/profile/{user_id}")
async def get_user_profile(user_id: int):
    """Get user profile"""
    user = auth_service.get_user_profile(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return success_response(data=user, message="User profile retrieved successfully")