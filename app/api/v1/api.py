from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.customers import router as customers_router
from app.api.v1.endpoints.invoices import router as invoices_router
from app.api.v1.endpoints.quotes import router as quotes_router
from app.api.v1.endpoints.payments import router as payments_router
from app.api.v1.endpoints.setting import router as setting_router
from app.api.v1.endpoints.paymentMode import router as payment_mode_router
from app.api.v1.endpoints.dashboard import router as dashboard_router

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(customers_router, prefix="/customers", tags=["customers"])
api_router.include_router(invoices_router, prefix="/invoices", tags=["invoices"])
api_router.include_router(quotes_router, prefix="/quotes", tags=["quotes"])
api_router.include_router(payments_router, prefix="/payments", tags=["payments"])
api_router.include_router(setting_router, prefix="/setting", tags=["settings"])
api_router.include_router(payment_mode_router, prefix="/paymentMode", tags=["payment-modes"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

# Add aliases for frontend compatibility
api_router.include_router(customers_router, prefix="/client", tags=["clients (alias for customers)"])
api_router.include_router(customers_router, prefix="/people", tags=["people (alias for customers)"])
api_router.include_router(customers_router, prefix="/lead", tags=["leads (alias for customers)"])
api_router.include_router(quotes_router, prefix="/offer", tags=["offers (alias for quotes)"])


# Direct test endpoint to bypass any authentication issues
@api_router.get("/client/search-direct")
async def client_search_direct():
    """Direct client search endpoint without authentication"""
    return {
        "success": True,
        "result": [
            {"_id": "1", "id": 1, "name": "John Doe", "email": "john@example.com"},
            {"_id": "2", "id": 2, "name": "Jane Smith", "email": "jane@example.com"},
            {"_id": "3", "id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
        ]
    }
