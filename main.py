from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import init_db
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

# Mount frontend app
app.mount("/", frontend_app)


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
async def client_search_main():
    """Client search endpoint directly in main app"""
    return {
        "success": True,
        "result": [
            {"_id": "1", "id": 1, "name": "John Doe", "email": "john@example.com"},
            {"_id": "2", "id": 2, "name": "Jane Smith", "email": "jane@example.com"},
            {"_id": "3", "id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
        ]
    }



