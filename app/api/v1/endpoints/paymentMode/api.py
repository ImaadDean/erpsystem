from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from supabase import Client
from app.core.database import get_supabase
from app.core.security import get_current_user

router = APIRouter()


@router.get("/")
async def list_payment_modes(
    skip: int = 0,
    limit: int = 100
):
    """Get all payment modes - no authentication required"""
    try:
        print("=== PAYMENT MODES LIST ENDPOINT CALLED ===")
        
        # Mock payment modes data
        mock_payment_modes = [
            {
                "_id": "1",
                "id": 1,
                "name": "Cash",
                "description": "Cash payment",
                "isActive": True,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "_id": "2",
                "id": 2,
                "name": "Credit Card",
                "description": "Credit card payment",
                "isActive": True,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "_id": "3",
                "id": 3,
                "name": "Bank Transfer",
                "description": "Bank transfer payment",
                "isActive": True,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "_id": "4",
                "id": 4,
                "name": "Check",
                "description": "Check payment",
                "isActive": True,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "_id": "5",
                "id": 5,
                "name": "PayPal",
                "description": "PayPal payment",
                "isActive": True,
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        # Apply pagination
        paginated_modes = mock_payment_modes[skip:skip + limit]
        
        print(f"Returning {len(paginated_modes)} payment modes")
        
        return {
            "success": True,
            "result": paginated_modes,
            "pagination": {
                "current": (skip // limit) + 1,
                "pageSize": limit,
                "total": len(mock_payment_modes)
            }
        }
        
    except Exception as e:
        print(f"Payment modes error: {e}")
        return {
            "success": True,
            "result": []
        }


@router.get("/{payment_mode_id}")
async def get_payment_mode(payment_mode_id: int):
    """Get a specific payment mode"""
    try:
        # Mock single payment mode
        mock_payment_mode = {
            "_id": str(payment_mode_id),
            "id": payment_mode_id,
            "name": "Cash" if payment_mode_id == 1 else f"Payment Mode {payment_mode_id}",
            "description": f"Payment mode {payment_mode_id} description",
            "isActive": True,
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        return {
            "success": True,
            "result": mock_payment_mode
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Payment mode not found"
        }


@router.post("/")
async def create_payment_mode(payment_mode_data: dict):
    """Create a new payment mode"""
    try:
        # Mock creation
        new_payment_mode = {
            "_id": "999",
            "id": 999,
            **payment_mode_data,
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        return {
            "success": True,
            "result": new_payment_mode,
            "message": "Payment mode created successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to create payment mode"
        }


@router.put("/{payment_mode_id}")
async def update_payment_mode(payment_mode_id: int, payment_mode_data: dict):
    """Update a payment mode"""
    try:
        # Mock update
        updated_payment_mode = {
            "_id": str(payment_mode_id),
            "id": payment_mode_id,
            **payment_mode_data,
            "updated_at": "2024-01-01T00:00:00Z"
        }
        
        return {
            "success": True,
            "result": updated_payment_mode,
            "message": "Payment mode updated successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to update payment mode"
        }


@router.delete("/{payment_mode_id}")
async def delete_payment_mode(payment_mode_id: int):
    """Delete a payment mode"""
    try:
        return {
            "success": True,
            "message": "Payment mode deleted successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to delete payment mode"
        }
