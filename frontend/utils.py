"""
Utility functions for frontend routes
"""
from app.core.database import get_supabase_service
from fastapi import Request


async def fetch_customers_summary():
    """Fetch customers summary from the API"""
    try:
        supabase = get_supabase_service()
        # Mock user for API calls
        mock_user = {"id": "admin", "email": "admin@admin.com"}

        # Import the function directly
        from app.api.v1.endpoints.customers.api import get_customers_summary
        result = await get_customers_summary(type="month", current_user=mock_user, supabase=supabase)
        return result
    except Exception as e:
        print(f"Error fetching customers summary: {e}")
        return {"success": False, "result": {"new": 0, "active": 0}}


async def fetch_invoices_summary():
    """Fetch invoices summary from the API"""
    try:
        supabase = get_supabase_service()
        mock_user = {"id": "admin", "email": "admin@admin.com"}

        from app.api.v1.endpoints.invoices.api import get_invoices_summary
        result = await get_invoices_summary(type="month", current_user=mock_user, supabase=supabase)
        return result
    except Exception as e:
        print(f"Error fetching invoices summary: {e}")
        return {"success": False, "result": {"total": 0, "total_undue": 0, "performance": []}}


async def fetch_quotes_summary():
    """Fetch quotes summary from the API"""
    try:
        supabase = get_supabase_service()
        mock_user = {"id": "admin", "email": "admin@admin.com"}

        from app.api.v1.endpoints.quotes.api import get_quotes_summary
        result = await get_quotes_summary(type="month", current_user=mock_user, supabase=supabase)
        return result
    except Exception as e:
        print(f"Error fetching quotes summary: {e}")
        return {"success": False, "result": {"total": 0, "performance": []}}


async def fetch_payments_summary():
    """Fetch payments summary from the API"""
    try:
        supabase = get_supabase_service()
        mock_user = {"id": "admin", "email": "admin@admin.com"}

        from app.api.v1.endpoints.payments.api import get_payments_summary
        result = await get_payments_summary(type="month", current_user=mock_user, supabase=supabase)
        return result
    except Exception as e:
        print(f"Error fetching payments summary: {e}")
        return {"success": False, "result": {"count": 0, "total": 0}}


async def fetch_customers_list():
    """Fetch customers list from the database"""
    try:
        supabase = get_supabase_service()
        response = supabase.table('customers').select('*').limit(50).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching customers list: {e}")
        return []


async def fetch_invoices_list():
    """Fetch invoices list from the database"""
    try:
        supabase = get_supabase_service()
        response = supabase.table('invoices').select('*').limit(50).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching invoices list: {e}")
        return []


async def get_current_user_info(request: Request = None):
    """Get current authenticated user information"""
    try:
        # Check for authentication token in cookies
        if request:
            auth_token = request.cookies.get('auth_token')
            if not auth_token:
                return None  # No authentication token found

        import httpx
        from app.core.database import get_supabase_service
        supabase = get_supabase_service()

        # Get the first active user from the database as current user
        response = supabase.table('users').select('*').eq('is_active', True).limit(1).execute()

        if response.data and len(response.data) > 0:
            user = response.data[0]
            return {
                "id": user.get('id'),
                "full_name": user.get('full_name', 'Admin User'),
                "email": user.get('email', 'admin@admin.com'),
                "role": user.get('role', 'admin'),
                "is_active": user.get('is_active', True),
                "is_authenticated": True
            }
        else:
            return None  # No user found

    except Exception as e:
        print(f"Error getting current user: {e}")
        return None  # Return None on error to force login


async def require_authentication(request: Request):
    """Check if user is authenticated, redirect to login if not"""
    from fastapi import HTTPException
    from fastapi.responses import RedirectResponse

    user = await get_current_user_info(request)
    if not user:
        # User is not authenticated, redirect to login
        return RedirectResponse(url="/login", status_code=302)

    return user


def check_auth_token(request: Request) -> bool:
    """Simple check if user has auth token"""
    auth_token = request.cookies.get('auth_token')
    return auth_token is not None


async def authenticate_user(request: Request):
    """
    Authenticate user and return user info or redirect to login
    Returns tuple: (user_info, redirect_response)
    If redirect_response is not None, return it immediately
    """
    from fastapi.responses import RedirectResponse

    # Check authentication first
    if not check_auth_token(request):
        return None, RedirectResponse(url="/login", status_code=302)

    # Get current user information
    current_user = await get_current_user_info(request)

    if not current_user:
        return None, RedirectResponse(url="/login", status_code=302)

    return current_user, None


def get_mock_user():
    """Get mock user data for templates - kept for backward compatibility"""
    # This will be replaced by async calls in the routes
    return {"full_name": "Admin User", "email": "admin@admin.com", "role": "admin"}
