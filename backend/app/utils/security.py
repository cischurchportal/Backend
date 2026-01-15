import hashlib
import secrets

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt (simplified for demo)"""
    # In production, use bcrypt or similar
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        salt, password_hash = hashed_password.split(':')
        return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
    except ValueError:
        # For backward compatibility with plain text passwords
        return password == hashed_password

def generate_token() -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)