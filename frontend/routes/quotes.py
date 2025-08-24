from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .utils import get_mock_user, get_current_user_info, authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/quotes", response_class=HTMLResponse)
async def quotes_page(request: Request):
    """Quotes list page"""
    # Authenticate user
    current_user, redirect_response = await authenticate_user(request)
    if redirect_response:
        return redirect_response

    return templates.TemplateResponse("quotes/list.html", {
        "request": request,
        "user": current_user
    })
