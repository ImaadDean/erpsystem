"""
Authentication routes for the ERP system frontend
"""
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    # If user is already logged in, redirect to dashboard
    auth_token = request.cookies.get('auth_token')
    if auth_token:
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request, "user": None})


@router.post("/login")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handle login form submission"""
    try:
        # Make request to our own login API
        async with httpx.AsyncClient() as client:
            login_response = await client.post(
                "http://localhost:8000/api/v1/auth/login",
                data={"username": username, "password": password}
            )

            if login_response.status_code == 200:
                # Login successful, set auth token
                auth_data = login_response.json()
                auth_token = auth_data.get('access_token', 'authenticated')

                # Create redirect response and set cookie
                response = RedirectResponse(url="/", status_code=302)
                response.set_cookie(
                    key="auth_token",
                    value=auth_token,
                    max_age=86400,  # 24 hours
                    httponly=True,
                    secure=False  # Set to True in production with HTTPS
                )
                return response
            else:
                # Login failed
                return templates.TemplateResponse("login.html", {
                    "request": request,
                    "error": "Invalid username or password",
                    "user": None
                })

    except Exception as e:
        print(f"Login error: {e}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Login failed. Please try again.",
            "user": None
        })


@router.get("/logout")
async def logout():
    """Logout and redirect to login"""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("auth_token")
    return response
