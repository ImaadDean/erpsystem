#!/usr/bin/env python3
"""
Script to create a test user in the database
"""
import asyncio
from app.core.database import get_supabase_service
from app.core.security import get_password_hash

async def create_test_user():
    """Create a test user in the database"""
    try:
        supabase = get_supabase_service()
        
        # Check if user already exists
        existing_user = supabase.table('users').select('*').eq('email', 'admin@admin.com').execute()
        
        if existing_user.data:
            print("✅ Test user already exists!")
            user = existing_user.data[0]
            print(f"   ID: {user['id']}")
            print(f"   Name: {user.get('full_name', 'N/A')}")
            print(f"   Email: {user['email']}")
            return user
        
        # Create test user
        hashed_password = get_password_hash("admin123")
        
        user_data = {
            "email": "admin@admin.com",
            "full_name": "System Administrator",
            "hashed_password": hashed_password,
            "is_active": True,
            "is_superuser": True,
            "role": "admin"
        }
        
        response = supabase.table('users').insert(user_data).execute()
        
        if response.data:
            user = response.data[0]
            print("✅ Test user created successfully!")
            print(f"   ID: {user['id']}")
            print(f"   Name: {user['full_name']}")
            print(f"   Email: {user['email']}")
            print(f"   Password: admin123")
            return user
        else:
            print("❌ Failed to create test user")
            return None
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(create_test_user())
