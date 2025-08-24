"""
Main FastAPI application for the ERP system frontend
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import auth, customers, invoices, payments, dashboard, settings, taxes, api

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="frontend/templates")

# Include routers
app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(payments.router)
app.include_router(dashboard.router)
app.include_router(settings.router)
app.include_router(taxes.router)
app.include_router(api.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})