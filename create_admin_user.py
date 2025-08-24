#!/usr/bin/env python3
"""
Create an admin user
"""
import asyncio
from app.core.database import get_supabase_service
from app.core.security import get_password_hash

async def create_admin_user():
    """Create an admin user"""
    try:
        supabase = get_supabase_service()
        
        # Admin user details - CHANGE THESE VALUES
        email = "admin@company.com"
        full_name = "System Administrator"
        password = "admin123456"  # Use a strong password in production
        
        print("Creating admin user...")
        print(f"Email: {email}")
        print(f"Name: {full_name}")
        
        # Check if user already exists
        existing_user = supabase.table('users').select('*').eq('email', email).execute()
        
        if existing_user.data:
            print(f"❌ Admin user with email {email} already exists!")
            user = existing_user.data[0]
            print(f"   Existing user ID: {user['id']}")
            print(f"   Name: {user.get('full_name', 'N/A')}")
            print(f"   Role: {user.get('role', 'user')}")
            return
        
        # Hash the password
        hashed_password = get_password_hash(password)
        
        # Create admin user data
        user_data = {
            "email": email,
            "full_name": full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_superuser": True,  # This makes the user an admin
            "role": "admin"
        }
        
        # Insert user into database
        response = supabase.table('users').insert(user_data).execute()
        
        if response.data:
            user = response.data[0]
            print("✅ Admin user created successfully!")
            print(f"   User ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Name: {user['full_name']}")
            print(f"   Role: {user.get('role', 'user')}")
            print(f"   Admin: {user['is_superuser']}")
            print(f"   Active: {user['is_active']}")
            
            print(f"\n🔑 Admin login credentials:")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"\n⚠️  IMPORTANT: Change the password after first login!")
            
        else:
            print("❌ Failed to create admin user")
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == "__main__":
    asyncio.run(create_admin_user())
