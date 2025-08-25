"""
Customer routes for the ERP system frontend
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from frontend.auth import get_current_user_from_cookie as get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/customers", response_class=HTMLResponse)
async def customers_page(request: Request, user: dict = Depends(get_current_user)):
    """Customers list page"""
    return templates.TemplateResponse("customers/list.html", {
        "request": request,
        "user": user
    })

@router.get("/customers/create", response_class=HTMLResponse)
async def create_customer_page(request: Request, user: dict = Depends(get_current_user)):
    """Create customer page"""
    return templates.TemplateResponse("customers/create.html", {
        "request": request,
        "user": user
    })

@router.get("/customers/{customer_id}", response_class=HTMLResponse)
async def view_customer_page(request: Request, customer_id: int, user: dict = Depends(get_current_user)):
    """View customer page"""
    return templates.TemplateResponse("customers/view.html", {
        "request": request,
        "customer_id": customer_id,
        "user": user
    })

@router.get("/clients-table", response_class=HTMLResponse)
async def clients_table_page(request: Request):
    """Clients table page (no auth required)"""
    # Mock user for template
    mock_user = {"id": 1, "name": "Demo User", "email": "demo@example.com"}
    return templates.TemplateResponse("customers/list.html", {
        "request": request,
        "user": mock_user
    })
