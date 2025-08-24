#!/usr/bin/env python3
"""
Test authentication flow
"""
import asyncio
import httpx

async def test_auth():
    """Test the authentication endpoints"""
    try:
        async with httpx.AsyncClient() as client:
            # Test login endpoint
            print("Testing login endpoint...")
            login_response = await client.post(
                "http://localhost:8000/api/v1/auth/login",
                data={"username": "admin@admin.com", "password": "admin123"}
            )
            
            print(f"Login response status: {login_response.status_code}")
            if login_response.status_code == 200:
                print("Login successful!")
                print(f"Response: {login_response.json()}")
            else:
                print(f"Login failed: {login_response.text}")
                
            # Test accessing payments page without auth
            print("\nTesting payments page without auth...")
            payments_response = await client.get("http://localhost:8000/payments")
            print(f"Payments response status: {payments_response.status_code}")
            print(f"Response headers: {dict(payments_response.headers)}")
            
            if payments_response.status_code == 302:
                print(f"Redirected to: {payments_response.headers.get('location')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_auth())
