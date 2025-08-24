"""
Frontend routes package for the ERP system
"""
from .dashboard import router as dashboard_router
from .auth import router as auth_router
from .customers import router as customers_router
from .invoices import router as invoices_router
from .payments import router as payments_router

__all__ = [
    "dashboard_router",
    "auth_router",
    "customers_router",
    "invoices_router",
    "payments_router"
]
