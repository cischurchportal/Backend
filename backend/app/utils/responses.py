from typing import Any, Dict
from fastapi import HTTPException
from fastapi.responses import JSONResponse

def success_response(
    data: Any = None, 
    message: str = "Success", 
    status_code: int = 200
) -> JSONResponse:
    """Create a standardized success response"""
    response_data = {
        "success": True,
        "message": message,
        "data": data
    }
    return JSONResponse(content=response_data, status_code=status_code)

def error_response(
    message: str, 
    status_code: int = 400, 
    details: Dict[str, Any] | None = None
) -> HTTPException:
    """Create a standardized error response"""
    error_data = {
        "success": False,
        "message": message
    }
    
    if details:
        error_data["details"] = details
    
    return HTTPException(status_code=status_code, detail=error_data)

def validation_error_response(errors: Dict[str, str]) -> HTTPException:
    """Create a validation error response"""
    return error_response(
        message="Validation failed",
        status_code=422,
        details={"validation_errors": errors}
    )

def not_found_response(resource: str = "Resource") -> HTTPException:
    """Create a not found error response"""
    return error_response(
        message=f"{resource} not found",
        status_code=404
    )

def unauthorized_response(message: str = "Unauthorized") -> HTTPException:
    """Create an unauthorized error response"""
    return error_response(
        message=message,
        status_code=401
    )

def forbidden_response(message: str = "Forbidden") -> HTTPException:
    """Create a forbidden error response"""
    return error_response(
        message=message,
        status_code=403
    )

def internal_server_error_response(message: str = "Internal server error") -> HTTPException:
    """Create an internal server error response"""
    return error_response(
        message=message,
        status_code=500
    )