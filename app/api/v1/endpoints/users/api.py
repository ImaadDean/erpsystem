from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client
from app.core.database import get_supabase
from app.core.security import get_current_user
from app.schemas.user import User, UserUpdate

router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update current user information"""
    try:
        update_data = user_update.dict(exclude_unset=True)
        
        response = supabase.table('users').update(update_data).eq('id', current_user['id']).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update user"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get all users (admin only)"""
    # Check if user is admin/superuser
    if current_user.get('is_superuser') != 'admin' and current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        response = supabase.table('users').select('*').range(skip, skip + limit - 1).execute()
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
