"""
Settings routes for the ERP system frontend
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from frontend.auth import get_current_user_from_cookie as get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, user: dict = Depends(get_current_user)):
    """Settings page"""
    return templates.TemplateResponse("settings/index.html", {
        "request": request,
        "user": user
    })

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request, user: dict = Depends(get_current_user)):
    """About page"""
    return templates.TemplateResponse("about/index.html", {
        "request": request,
        "user": user
    })
