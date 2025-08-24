#!/usr/bin/env python3
"""
Create a user using the API endpoint
"""
import asyncio
import httpx
import json

async def create_user_via_api():
    """Create a user using the registration API"""
    try:
        # User data
        user_data = {
            "email": "john.doe@example.com",
            "full_name": "John Doe",
            "password": "securepassword123"
        }
        
        print("Creating user via API...")
        print(f"Email: {user_data['email']}")
        print(f"Name: {user_data['full_name']}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/v1/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\nResponse Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ User created successfully!")
                print(f"User ID: {result.get('user_id')}")
                print(f"Message: {result.get('message')}")
                
                # Test login with the new user
                print("\n🔐 Testing login with new user...")
                login_response = await client.post(
                    "http://localhost:8000/api/v1/auth/login",
                    data={"username": user_data['email'], "password": user_data['password']}
                )
                
                if login_response.status_code == 200:
                    login_result = login_response.json()
                    print("✅ Login successful!")
                    print(f"Access Token: {login_result.get('access_token')[:50]}...")
                else:
                    print(f"❌ Login failed: {login_response.text}")
                    
            else:
                print(f"❌ User creation failed: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(create_user_via_api())
