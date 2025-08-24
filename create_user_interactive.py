#!/usr/bin/env python3
"""
Interactive user creation script
"""
import asyncio
import getpass
from app.core.database import get_supabase_service
from app.core.security import get_password_hash

async def create_user_interactive():
    """Create a user with interactive prompts"""
    try:
        supabase = get_supabase_service()
        
        print("=== ERP System User Creation ===\n")
        
        # Get user input
        email = input("Enter email address: ").strip()
        if not email:
            print("❌ Email is required!")
            return
            
        full_name = input("Enter full name: ").strip()
        if not full_name:
            print("❌ Full name is required!")
            return
            
        password = getpass.getpass("Enter password: ")
        if not password:
            print("❌ Password is required!")
            return
            
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("❌ Passwords don't match!")
            return
            
        is_admin_input = input("Make user admin? (y/N): ").strip().lower()
        is_admin = is_admin_input in ['y', 'yes']
        
        print(f"\n📋 User Details:")
        print(f"   Email: {email}")
        print(f"   Name: {full_name}")
        print(f"   Admin: {'Yes' if is_admin else 'No'}")
        
        confirm = input("\nCreate this user? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ User creation cancelled.")
            return
        
        # Check if user already exists
        existing_user = supabase.table('users').select('*').eq('email', email).execute()
        
        if existing_user.data:
            print(f"❌ User with email {email} already exists!")
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
            print("\n✅ User created successfully!")
            print(f"   User ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Name: {user['full_name']}")
            print(f"   Role: {user.get('role', 'user')}")
            
            print(f"\n🔑 The user can now login with:")
            print(f"   Email: {email}")
            print(f"   Password: [the password you entered]")
            
        else:
            print("❌ Failed to create user")
            
    except KeyboardInterrupt:
        print("\n❌ User creation cancelled.")
    except Exception as e:
        print(f"❌ Error creating user: {e}")

if __name__ == "__main__":
    asyncio.run(create_user_interactive())
