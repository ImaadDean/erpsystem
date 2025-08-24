"""
User management utilities and helper functions
"""

from typing import Dict, List, Optional
from uuid import UUID


def format_user_response(user_data: dict) -> dict:
    """Format user data for API response"""
    return {
        "id": user_data.get("id"),
        "email": user_data.get("email"),
        "full_name": user_data.get("full_name"),
        "is_active": user_data.get("is_active", True),
        "is_superuser": user_data.get("is_superuser", False),
        "created_at": user_data.get("created_at"),
        "updated_at": user_data.get("updated_at")
    }


def validate_user_permissions(current_user: dict, required_role: str = "user") -> bool:
    """Validate user permissions"""
    if required_role == "admin":
        return current_user.get("is_superuser", False)
    return current_user.get("is_active", False)


def filter_user_data(user_data: dict, include_sensitive: bool = False) -> dict:
    """Filter user data based on permissions"""
    filtered_data = {
        "id": user_data.get("id"),
        "email": user_data.get("email"),
        "full_name": user_data.get("full_name"),
        "is_active": user_data.get("is_active"),
        "created_at": user_data.get("created_at"),
        "updated_at": user_data.get("updated_at")
    }
    
    if include_sensitive:
        filtered_data["is_superuser"] = user_data.get("is_superuser", False)
    
    return filtered_data


def prepare_user_update(update_data: dict) -> dict:
    """Prepare user data for update operation"""
    allowed_fields = ["email", "full_name", "is_active"]
    return {k: v for k, v in update_data.items() if k in allowed_fields and v is not None}
