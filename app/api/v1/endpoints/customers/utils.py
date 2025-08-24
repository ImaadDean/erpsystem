"""
Customer management utilities and helper functions
"""

from typing import Dict, List, Optional


def format_customer_response(customer_data: dict) -> dict:
    """Format customer data for API response"""
    return {
        "id": customer_data.get("id"),
        "name": customer_data.get("name"),
        "email": customer_data.get("email"),
        "phone": customer_data.get("phone"),
        "address": customer_data.get("address"),
        "city": customer_data.get("city"),
        "state": customer_data.get("state"),
        "country": customer_data.get("country"),
        "postal_code": customer_data.get("postal_code"),
        "tax_number": customer_data.get("tax_number"),
        "notes": customer_data.get("notes"),
        "created_by": customer_data.get("created_by"),
        "created_at": customer_data.get("created_at"),
        "updated_at": customer_data.get("updated_at")
    }


def validate_customer_data(customer_data: dict) -> dict:
    """Validate and clean customer data"""
    required_fields = ["name"]
    
    for field in required_fields:
        if not customer_data.get(field):
            raise ValueError(f"Field '{field}' is required")
    
    # Clean and validate email if provided
    if customer_data.get("email"):
        email = customer_data["email"].strip().lower()
        if "@" not in email:
            raise ValueError("Invalid email format")
        customer_data["email"] = email
    
    # Clean phone number if provided
    if customer_data.get("phone"):
        customer_data["phone"] = customer_data["phone"].strip()
    
    return customer_data


def prepare_customer_search_query(search_term: str) -> str:
    """Prepare search query for customer search"""
    # This would be used with database search functionality
    return f"%{search_term.lower()}%"


def filter_customer_fields(customer_data: dict, include_sensitive: bool = True) -> dict:
    """Filter customer fields based on permissions"""
    public_fields = [
        "id", "name", "email", "phone", "city", "state", "country", 
        "created_at", "updated_at"
    ]
    
    if include_sensitive:
        public_fields.extend(["address", "postal_code", "tax_number", "notes"])
    
    return {k: v for k, v in customer_data.items() if k in public_fields}
