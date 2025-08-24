from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from supabase import Client
from app.core.database import get_supabase, get_supabase_service
from app.core.security import get_current_user
from app.schemas.payment import Payment, PaymentCreate, PaymentUpdate
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/summary")
async def get_payments_summary(
    type: str = "month",
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_service)
):
    """Get payments summary statistics"""
    try:
        # Calculate date range based on type
        now = datetime.now()
        if type == "week":
            start_date = now - timedelta(weeks=1)
        elif type == "year":
            start_date = now - timedelta(days=365)
        else:  # default to month
            start_date = now - timedelta(days=30)

        # Get all payments in the period
        response = supabase.table('payments').select('*').gte('created_at', start_date.isoformat()).execute()
        payments = response.data

        # Calculate totals
        total_amount = sum(float(payment.get('amount', 0)) for payment in payments)
        count = len(payments)

        return {
            "success": True,
            "result": {
                "count": count,
                "total": total_amount
            },
            "message": f"Successfully get summary of payments for the last {type}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/", response_model=Payment)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Create a new payment"""
    try:
        payment_dict = payment_data.dict()
        payment_dict['created_by'] = current_user['id']
        payment_dict['status'] = 'pending'
        
        response = supabase.table('payments').insert(payment_dict).execute()
        
        if response.data:
            # Update invoice payment status if applicable
            if payment_data.invoice_id:
                # Get current invoice
                invoice_response = supabase.table('invoices').select('*').eq('id', payment_data.invoice_id).execute()
                if invoice_response.data:
                    invoice = invoice_response.data[0]
                    # Calculate total payments for this invoice
                    payments_response = supabase.table('payments').select('amount').eq('invoice_id', payment_data.invoice_id).eq('status', 'completed').execute()
                    total_paid = sum(p['amount'] for p in payments_response.data) + payment_data.amount
                    
                    # Update invoice status based on payment
                    if total_paid >= invoice['total_amount']:
                        supabase.table('invoices').update({'status': 'paid'}).eq('id', payment_data.invoice_id).execute()
                    else:
                        supabase.table('invoices').update({'status': 'partially_paid'}).eq('id', payment_data.invoice_id).execute()
            
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create payment"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Payment])
async def get_payments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    invoice_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get all payments"""
    try:
        query = supabase.table('payments').select('*, invoices(*), customers(*)')
        
        if status:
            query = query.eq('status', status)
        
        if invoice_id:
            query = query.eq('invoice_id', invoice_id)
            
        if customer_id:
            query = query.eq('customer_id', customer_id)
        
        response = query.range(skip, skip + limit - 1).execute()
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{payment_id}", response_model=Payment)
async def get_payment(
    payment_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get a specific payment"""
    try:
        response = supabase.table('payments').select('*, invoices(*), customers(*)').eq('id', payment_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{payment_id}", response_model=Payment)
async def update_payment(
    payment_id: int,
    payment_update: PaymentUpdate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update a payment"""
    try:
        update_data = payment_update.dict(exclude_unset=True)
        
        response = supabase.table('payments').update(update_data).eq('id', payment_id).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{payment_id}/confirm")
async def confirm_payment(
    payment_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Confirm a payment"""
    try:
        response = supabase.table('payments').update({'status': 'completed'}).eq('id', payment_id).execute()
        
        if response.data:
            return {"message": "Payment confirmed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



