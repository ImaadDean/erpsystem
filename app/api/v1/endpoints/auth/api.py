from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from supabase import Client
from app.core.database import get_supabase, get_supabase_service
from app.core.security import verify_password, create_access_token, get_password_hash
from app.schemas.auth import Token, UserCreate, UserLogin
from app.schemas.user import User
from datetime import timedelta
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=dict)
async def register(
    user_data: UserCreate,
    supabase: Client = Depends(get_supabase_service)  # Use service client for registration
):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = supabase.table('users').select('*').eq('email', user_data.email).execute()
        if existing_user.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user - let PostgreSQL generate the UUID
        user_dict = {
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_superuser": False
        }
        
        response = supabase.table('users').insert(user_dict).execute()
        
        if response.data:
            return {"message": "User created successfully", "user_id": response.data[0]['id']}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")  # For debugging
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    supabase: Client = Depends(get_supabase)
):
    """Login user and return access token"""
    try:
        # Get user by email
        response = supabase.table('users').select('*').eq('email', form_data.username).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        user = response.data[0]
        
        # Verify password
        if not verify_password(form_data.password, user['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is active
        if not user.get('is_active', True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": str(user['id']),
                "email": user['email'],
                "role": user.get('role', 'user'),
                "is_superuser": user.get('is_superuser', 'user')
            },
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
