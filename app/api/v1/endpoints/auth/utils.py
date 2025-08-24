"""
Authentication utilities and helper functions
"""

from typing import Optional
from datetime import datetime, timedelta
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings


def generate_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generate access token for user"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return create_access_token(data={"sub": user_id}, expires_delta=expires_delta)


def validate_password(plain_password: str, hashed_password: str) -> bool:
    """Validate password against hash"""
    return verify_password(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a password"""
    return get_password_hash(password)


def prepare_user_response(user_data: dict) -> dict:
    """Prepare user data for API response"""
    return {
        "id": user_data.get("id"),
        "email": user_data.get("email"),
        "full_name": user_data.get("full_name"),
        "is_active": user_data.get("is_active", True),
        "is_superuser": user_data.get("is_superuser", False),
        "created_at": user_data.get("created_at"),
        "updated_at": user_data.get("updated_at")
    }
