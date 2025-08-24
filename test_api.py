"""
Simple test script to verify the API is working
Run this after setting up the environment and database
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")

def test_root_endpoint():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")

def test_register_user():
    """Test user registration"""
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
    print(f"User registration: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_login_user():
    """Test user login"""
    login_data = {
        "username": "test@example.com",  # OAuth2PasswordRequestForm uses 'username' field
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
    print(f"User login: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Access token received: {token_data['token_type']} {token_data['access_token'][:20]}...")
        return token_data['access_token']
    else:
        print(f"Login failed: {response.json()}")
        return None

def test_protected_endpoint(token):
    """Test accessing a protected endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
    print(f"Protected endpoint: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    print("Testing ERP System API...")
    print("=" * 50)
    
    # Test basic endpoints
    test_health_check()
    test_root_endpoint()
    
    print("\nTesting authentication...")
    print("-" * 30)
    
    # Test registration (might fail if user already exists)
    test_register_user()
    
    # Test login
    token = test_login_user()
    
    if token:
        print("\nTesting protected endpoints...")
        print("-" * 30)
        test_protected_endpoint(token)
    
    print("\nAPI testing completed!")
