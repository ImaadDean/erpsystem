"""
Taxes routes for the ERP system frontend
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from frontend.auth import get_current_user_from_cookie as get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/taxes", response_class=HTMLResponse)
async def taxes_page(request: Request, user: dict = Depends(get_current_user)):
    """Taxes management page"""
    return templates.TemplateResponse("taxes/list.html", {
        "request": request,
        "user": user
    })

@router.get("/payment-modes", response_class=HTMLResponse)
async def payment_modes_page(request: Request, user: dict = Depends(get_current_user)):
    """Payment modes management page"""
    return templates.TemplateResponse("payment_modes/list.html", {
        "request": request,
        "user": user
    })
