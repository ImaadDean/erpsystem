"""
Invoice routes for the ERP system frontend
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from frontend.auth import get_current_user_from_cookie as get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/invoices", response_class=HTMLResponse)
async def invoices_page(request: Request, user: dict = Depends(get_current_user)):
    """Invoices list page"""
    return templates.TemplateResponse("invoices/list.html", {
        "request": request,
        "user": user
    })
