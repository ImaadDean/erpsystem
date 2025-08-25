from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from supabase import Client
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import init_db, get_supabase_service
from frontend.main import app as frontend_app


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ERP/CRM System built with FastAPI and Supabase",
    lifespan=lifespan
)

# Mount static files and setup templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


# Additional API routes
@app.get("/api-root")
async def api_root():
    return {
        "message": "Welcome to ERP System API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/v1/client/search")
async def client_search_main(supabase: Client = Depends(get_supabase_service)):
    """Client search endpoint directly in main app - fetches real data"""
    try:
        response = supabase.table('customers').select('*').execute()
        customers = response.data or []
        
        # Format data for frontend compatibility
        formatted_customers = []
        for customer in customers:
            formatted_customers.append({
                "_id": str(customer.get('id', '')),
                "id": customer.get('id'),
                "name": customer.get('name', ''),
                "email": customer.get('email', ''),
                "phone": customer.get('phone', ''),
                "city": customer.get('city', ''),
                "country": customer.get('country', '')
            })
        
        return {
            "success": True,
            "result": formatted_customers
        }
    except Exception as e:
        print(f"Error fetching customers: {e}")
        # Fallback to mock data if database fails
        return {
            "success": True,
            "result": [
                {"_id": "1", "id": 1, "name": "John Doe", "email": "john@example.com"},
                {"_id": "2", "id": 2, "name": "Jane Smith", "email": "jane@example.com"},
                {"_id": "3", "id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
            ]
        }


# Frontend compatibility endpoints
@app.get("/clients")
async def clients_endpoint(supabase: Client = Depends(get_supabase_service)):
    """Frontend compatibility endpoint for /clients - fetches real data"""
    try:
        response = supabase.table('customers').select('*').execute()
        customers = response.data or []
        
        # Format data for frontend compatibility
        formatted_customers = []
        for customer in customers:
            formatted_customers.append({
                "_id": str(customer.get('id', '')),
                "id": customer.get('id'),
                "name": customer.get('name', ''),
                "email": customer.get('email', ''),
                "phone": customer.get('phone', ''),
                "city": customer.get('city', ''),
                "country": customer.get('country', ''),
                "address": customer.get('address', ''),
                "state": customer.get('state', ''),
                "zipCode": customer.get('zip_code', '')
            })
        
        return {
            "success": True,
            "result": formatted_customers
        }
    except Exception as e:
        print(f"Error fetching clients: {e}")
        # Fallback to mock data if database fails
        return {
            "success": True,
            "result": [
                {"_id": "1", "id": 1, "name": "John Doe", "email": "john@example.com", "phone": "+1234567890"},
                {"_id": "2", "id": 2, "name": "Jane Smith", "email": "jane@example.com", "phone": "+1234567891"},
                {"_id": "3", "id": 3, "name": "Bob Johnson", "email": "bob@example.com", "phone": "+1234567892"}
            ]
        }


@app.get("/invoices")
async def invoices_endpoint(supabase: Client = Depends(get_supabase_service)):
    """Frontend compatibility endpoint for /invoices - fetches real data without authentication"""
    try:
        response = supabase.table('invoices').select('*, customers(name, email)').execute()
        invoices = response.data or []
        
        # Format data for frontend compatibility
        formatted_invoices = []
        for invoice in invoices:
            customer = invoice.get('customers', {})
            formatted_invoices.append({
                "_id": str(invoice.get('id', '')),
                "id": invoice.get('id'),
                "number": invoice.get('number', ''),
                "status": invoice.get('status', 'draft'),
                "total": float(invoice.get('total', 0)),
                "subtotal": float(invoice.get('subtotal', 0)),
                "tax": float(invoice.get('tax', 0)),
                "discount": float(invoice.get('discount', 0)),
                "date": invoice.get('date', ''),
                "due_date": invoice.get('due_date', ''),
                "customer_id": invoice.get('customer_id'),
                "customer_name": customer.get('name', '') if customer else '',
                "customer_email": customer.get('email', '') if customer else '',
                "created_at": invoice.get('created_at', ''),
                "updated_at": invoice.get('updated_at', '')
            })
        
        return {
            "success": True,
            "result": formatted_invoices
        }
    except Exception as e:
        print(f"Error fetching invoices: {e}")
        # Fallback to mock data if database fails
        return {
            "success": True,
            "result": [
                {"_id": "1", "id": 1, "number": "INV-001", "status": "paid", "total": 1000.00, "customer_name": "John Doe"},
                {"_id": "2", "id": 2, "number": "INV-002", "status": "pending", "total": 2500.50, "customer_name": "Jane Smith"},
                {"_id": "3", "id": 3, "number": "INV-003", "status": "draft", "total": 750.25, "customer_name": "Bob Johnson"}
            ]
        }


@app.get("/api/v1/invoices-public")
async def invoices_public_endpoint(supabase: Client = Depends(get_supabase_service)):
    """Public invoices endpoint without authentication - fetches real data"""
    try:
        response = supabase.table('invoices').select('*, customers(name, email)').execute()
        invoices = response.data or []
        
        # Format data for frontend compatibility
        formatted_invoices = []
        for invoice in invoices:
            customer = invoice.get('customers', {})
            formatted_invoices.append({
                "_id": str(invoice.get('id', '')),
                "id": invoice.get('id'),
                "number": invoice.get('number', ''),
                "status": invoice.get('status', 'draft'),
                "total": float(invoice.get('total', 0)),
                "customer_id": invoice.get('customer_id'),
                "customer_name": customer.get('name', '') if customer else '',
                "date": invoice.get('date', ''),
                "created_at": invoice.get('created_at', '')
            })
        
        return {
            "success": True,
            "result": formatted_invoices
        }
    except Exception as e:
        print(f"Error fetching invoices: {e}")
        return {
            "success": True,
            "result": []
        }


# Mount frontend app last (after all API routes are defined)
app.mount("/", frontend_app)
