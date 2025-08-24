"""
Payment Mode utilities and helper functions
"""

from typing import Dict, List


def get_default_payment_modes() -> List[Dict]:
    """Get default payment modes"""
    return [
        {"name": "Cash", "description": "Cash payment", "isActive": True},
        {"name": "Credit Card", "description": "Credit card payment", "isActive": True},
        {"name": "Bank Transfer", "description": "Bank transfer payment", "isActive": True},
        {"name": "Check", "description": "Check payment", "isActive": True},
        {"name": "PayPal", "description": "PayPal payment", "isActive": True}
    ]


def validate_payment_mode_data(data: Dict) -> bool:
    """Validate payment mode data"""
    required_fields = ["name"]
    return all(field in data for field in required_fields)


def format_payment_mode_response(payment_mode: Dict) -> Dict:
    """Format payment mode for API response"""
    return {
        "_id": str(payment_mode.get("id", "")),
        "id": payment_mode.get("id"),
        "name": payment_mode.get("name"),
        "description": payment_mode.get("description", ""),
        "isActive": payment_mode.get("isActive", True),
        "created_at": payment_mode.get("created_at"),
        "updated_at": payment_mode.get("updated_at")
    }
