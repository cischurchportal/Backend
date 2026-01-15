import re
from datetime import datetime
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Simple validation for various phone formats
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    return re.match(pattern, cleaned_phone) is not None

def validate_datetime_iso(datetime_str: str) -> bool:
    """Validate ISO datetime format"""
    try:
        datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def validate_date_iso(date_str: str) -> bool:
    """Validate ISO date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_positive_number(value: float) -> bool:
    """Validate that a number is positive"""
    return value > 0

def validate_username(username: str) -> tuple[bool, str | None]:
    """Validate username format and return (is_valid, error_message)"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, None

def validate_password(password: str) -> tuple[bool, str | None]:
    """Validate password strength and return (is_valid, error_message)"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    # Check for at least one uppercase, lowercase, and number
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None

def sanitize_string(value: str, max_length: int | None = None) -> str:
    """Sanitize string input"""
    # Remove leading/trailing whitespace
    sanitized = value.strip()
    
    # Truncate if max_length specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized