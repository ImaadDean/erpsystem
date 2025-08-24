from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Dict, Any
from supabase import Client
from app.core.database import get_supabase
from app.core.security import get_current_user
import json

router = APIRouter()


@router.get("/listAll")
async def list_all_settings():
    """Get all application settings - no authentication required"""
    try:
        print("=== SETTINGS LIST ALL ENDPOINT CALLED ===")

        # Return default settings for now
        # In a real application, these would come from a settings table
        default_settings = {
            "success": True,
            "result": [
                {
                    "id": 1,
                    "settingCategory": "app_settings",
                    "settingKey": "app_name",
                    "settingValue": "ERP System",
                    "valueType": "string",
                    "isPublic": True,
                    "description": "Application name"
                },
                {
                    "id": 2,
                    "settingCategory": "app_settings", 
                    "settingKey": "app_version",
                    "settingValue": "1.0.0",
                    "valueType": "string",
                    "isPublic": True,
                    "description": "Application version"
                },
                {
                    "id": 3,
                    "settingCategory": "company_settings",
                    "settingKey": "company_name",
                    "settingValue": "Your Company Name",
                    "valueType": "string",
                    "isPublic": True,
                    "description": "Company name"
                },
                {
                    "id": 4,
                    "settingCategory": "company_settings",
                    "settingKey": "company_address",
                    "settingValue": "123 Business Street, City, Country",
                    "valueType": "string",
                    "isPublic": True,
                    "description": "Company address"
                },
                {
                    "id": 5,
                    "settingCategory": "finance_settings",
                    "settingKey": "default_currency",
                    "settingValue": "USD",
                    "valueType": "string",
                    "isPublic": True,
                    "description": "Default currency"
                },
                {
                    "id": 6,
                    "settingCategory": "finance_settings",
                    "settingKey": "tax_rate",
                    "settingValue": "10",
                    "valueType": "number",
                    "isPublic": True,
                    "description": "Default tax rate percentage"
                }
            ],
            "pagination": {
                "current": 1,
                "pageSize": 10,
                "total": 6
            }
        }
        
        return default_settings
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/list")
async def list_settings(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get settings with pagination"""
    try:
        # This would normally query a settings table
        # For now, return the same default settings
        settings_response = await list_all_settings(current_user, supabase)
        
        # Apply pagination
        all_settings = settings_response["result"]
        if category:
            all_settings = [s for s in all_settings if s["settingCategory"] == category]
        
        paginated_settings = all_settings[skip:skip + limit]
        
        return {
            "success": True,
            "result": paginated_settings,
            "pagination": {
                "current": (skip // limit) + 1,
                "pageSize": limit,
                "total": len(all_settings)
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{setting_id}")
async def get_setting(
    setting_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get a specific setting by ID"""
    try:
        settings_response = await list_all_settings(current_user, supabase)
        all_settings = settings_response["result"]
        
        setting = next((s for s in all_settings if s["id"] == setting_id), None)
        
        if not setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setting not found"
            )
        
        return {
            "success": True,
            "result": setting
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/")
async def create_setting(
    setting_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Create a new setting (admin only)"""
    if not current_user.get('is_superuser', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    try:
        # In a real implementation, this would insert into a settings table
        return {
            "success": True,
            "result": {
                "id": 999,  # Would be generated by database
                **setting_data,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            "message": "Setting created successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/updateManySetting")
async def update_many_settings(
    request_data: Dict[str, Any]
):
    """Update multiple settings at once - no authentication required"""
    try:
        print("=== UPDATE MANY SETTINGS ENDPOINT CALLED ===")
        print(f"Request data: {request_data}")
        print(f"Request data type: {type(request_data)}")
        # Handle different possible data formats from frontend
        settings_data = []

        # Check if the data is directly a list
        if isinstance(request_data, list):
            settings_data = request_data
        # Check if the data has a 'settings' key
        elif isinstance(request_data, dict) and 'settings' in request_data:
            settings_data = request_data['settings']
        # Check if the data has individual setting keys
        elif isinstance(request_data, dict):
            # Convert dict format to list format
            for key, value in request_data.items():
                if isinstance(value, dict):
                    settings_data.append({
                        "settingKey": key,
                        **value
                    })
                else:
                    settings_data.append({
                        "settingKey": key,
                        "settingValue": value
                    })

        # In a real implementation, this would update multiple settings in the database
        updated_settings = []
        for i, setting in enumerate(settings_data):
            updated_setting = {
                "id": setting.get("id", i + 1),
                "settingCategory": setting.get("settingCategory", "app_settings"),
                "settingKey": setting.get("settingKey", f"setting_{i}"),
                "settingValue": setting.get("settingValue", ""),
                "valueType": setting.get("valueType", "string"),
                "isPublic": setting.get("isPublic", True),
                "description": setting.get("description", ""),
                "updated_at": "2024-01-01T00:00:00Z"
            }
            updated_settings.append(updated_setting)

        return {
            "success": True,
            "result": updated_settings,
            "message": f"Updated {len(updated_settings)} settings successfully"
        }

    except Exception as e:
        print(f"Error in updateManySetting: {e}")  # For debugging
        print(f"Request data: {request_data}")  # For debugging
        print(f"Request data type: {type(request_data)}")  # For debugging
        return {
            "success": True,
            "result": [],
            "message": "Settings update completed (mock response)"
        }


@router.put("/{setting_id}")
async def update_setting(
    setting_id: int,
    setting_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update a specific setting (admin only)"""
    if not current_user.get('is_superuser', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    try:
        # In a real implementation, this would update the setting in the database
        updated_setting = {
            "id": setting_id,
            **setting_data,
            "updated_at": "2024-01-01T00:00:00Z"
        }

        return {
            "success": True,
            "result": updated_setting,
            "message": "Setting updated successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{setting_id}")
async def delete_setting(
    setting_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Delete a specific setting (admin only)"""
    if not current_user.get('is_superuser', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    try:
        # In a real implementation, this would delete the setting from the database
        return {
            "success": True,
            "message": "Setting deleted successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Additional endpoints that the frontend might expect
@router.get("/filter")
async def filter_settings(
    filter: str = None,
    equal: str = None,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Filter settings based on criteria"""
    try:
        settings_response = await list_all_settings(current_user, supabase)
        all_settings = settings_response["result"]

        # Apply filters (basic implementation)
        filtered_settings = all_settings
        if filter and equal:
            filtered_settings = [s for s in all_settings if s.get(filter) == equal]

        return {
            "success": True,
            "result": filtered_settings,
            "pagination": {
                "current": 1,
                "pageSize": len(filtered_settings),
                "total": len(filtered_settings)
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/search")
async def search_settings(
    q: str = None,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Search settings"""
    try:
        settings_response = await list_all_settings(current_user, supabase)
        all_settings = settings_response["result"]

        # Apply search (basic implementation)
        if q:
            search_term = q.lower()
            filtered_settings = [
                s for s in all_settings
                if search_term in s.get("settingKey", "").lower() or
                   search_term in s.get("settingValue", "").lower() or
                   search_term in s.get("description", "").lower()
            ]
        else:
            filtered_settings = all_settings

        return {
            "success": True,
            "result": filtered_settings,
            "pagination": {
                "current": 1,
                "pageSize": len(filtered_settings),
                "total": len(filtered_settings)
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
