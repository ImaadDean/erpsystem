from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Optional
from supabase import Client
from app.core.database import get_supabase, get_supabase_service
from app.core.security import get_current_user
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/summary")
async def get_customers_summary(
    type: str = "month",
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_service)
):
    """Get customers summary statistics"""
    try:
        # Calculate date range based on type
        now = datetime.now()
        if type == "week":
            start_date = now - timedelta(weeks=1)
        elif type == "year":
            start_date = now - timedelta(days=365)
        else:  # default to month
            start_date = now - timedelta(days=30)

        # Get total customers
        total_response = supabase.table('customers').select('id').execute()
        total_customers = len(total_response.data) if total_response.data else 0

        # Get new customers in the period
        new_response = supabase.table('customers').select('id').gte('created_at', start_date.isoformat()).execute()
        new_customers = len(new_response.data) if new_response.data else 0

        # Calculate active percentage (customers with recent activity)
        # For now, we'll consider all customers as potentially active
        active_customers = total_customers  # You can add more sophisticated logic here
        active_percentage = round((active_customers / total_customers * 100) if total_customers > 0 else 0)

        return {
            "success": True,
            "result": {
                "total": total_customers,
                "new": new_customers,
                "active": active_customers,
                "active_percentage": active_percentage
            },
            "message": f"Successfully get summary of customers for the last {type}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/", response_model=Customer)
async def create_customer(
    customer_data: CustomerCreate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Create a new customer"""
    try:
        customer_dict = customer_data.dict()
        customer_dict['created_by'] = current_user['id']
        
        response = supabase.table('customers').insert(customer_dict).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create customer"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Customer])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get all customers"""
    try:
        query = supabase.table('customers').select('*')

        if search:
            query = query.or_(f"name.ilike.%{search}%,email.ilike.%{search}%")

        response = query.range(skip, skip + limit - 1).execute()
        return response.data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/search")
async def search_customers():
    """Search customers - completely flexible endpoint"""
    try:
        print("=== CUSTOMER SEARCH ENDPOINT CALLED ===")

        # Mock search results - using _id format that frontend expects
        mock_customers = [
            {
                "_id": "1",
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "city": "New York",
                "country": "USA"
            },
            {
                "_id": "2",
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "+1234567891",
                "city": "Los Angeles",
                "country": "USA"
            },
            {
                "_id": "3",
                "id": 3,
                "name": "Bob Johnson",
                "email": "bob@example.com",
                "phone": "+1234567892",
                "city": "Chicago",
                "country": "USA"
            }
        ]

        print(f"Returning {len(mock_customers)} customers")

        return {
            "success": True,
            "result": mock_customers
        }

    except Exception as e:
        print(f"Search error: {e}")
        return {
            "success": True,
            "result": []
        }


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get a specific customer"""
    try:
        response = supabase.table('customers').select('*').eq('id', customer_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update a customer"""
    try:
        update_data = customer_update.dict(exclude_unset=True)
        
        response = supabase.table('customers').update(update_data).eq('id', customer_id).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Delete a customer"""
    try:
        response = supabase.table('customers').delete().eq('id', customer_id).execute()

        if response.data:
            return {"message": "Customer deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


