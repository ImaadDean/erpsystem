#!/usr/bin/env python3
"""
Create a user directly in the database
"""
import asyncio
from app.core.database import get_supabase_service
from app.core.security import get_password_hash

async def create_user_direct():
    """Create a user directly in the database"""
    try:
        supabase = get_supabase_service()
        
        # User details - CHANGE THESE VALUES
        email = "jane.smith@example.com"
        full_name = "Jane Smith"
        password = "mypassword123"
        is_admin = False  # Set to True to make user an admin
        
        print("Creating user directly in database...")
        print(f"Email: {email}")
        print(f"Name: {full_name}")
        print(f"Admin: {is_admin}")
        
        # Check if user already exists
        existing_user = supabase.table('users').select('*').eq('email', email).execute()
        
        if existing_user.data:
            print(f"❌ User with email {email} already exists!")
            user = existing_user.data[0]
            print(f"   Existing user ID: {user['id']}")
            print(f"   Name: {user.get('full_name', 'N/A')}")
            return
        
        # Hash the password
        hashed_password = get_password_hash(password)
        
        # Create user data
        user_data = {
            "email": email,
            "full_name": full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_superuser": is_admin,
            "role": "admin" if is_admin else "user"
        }
        
        # Insert user into database
        response = supabase.table('users').insert(user_data).execute()
        
        if response.data:
            user = response.data[0]
            print("✅ User created successfully!")
            print(f"   User ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Name: {user['full_name']}")
            print(f"   Role: {user.get('role', 'user')}")
            print(f"   Active: {user['is_active']}")
            
            print(f"\n🔑 Login credentials:")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            
        else:
            print("❌ Failed to create user")
            
    except Exception as e:
        print(f"❌ Error creating user: {e}")

if __name__ == "__main__":
    asyncio.run(create_user_direct())
