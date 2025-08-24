"""
Dashboard routes for the ERP system frontend
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from frontend.auth import get_current_user_from_cookie as get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request, user: dict = Depends(get_current_user)):
    """Dashboard page"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user
    })
