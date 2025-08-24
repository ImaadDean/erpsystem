from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from supabase import Client
from app.core.database import get_supabase, get_supabase_service
from app.core.security import get_current_user
from app.schemas.invoice import Invoice, InvoiceCreate, InvoiceUpdate
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/summary")
async def get_invoices_summary(
    type: str = "month",
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_service)
):
    """Get invoices summary statistics"""
    try:
        # Calculate date range based on type
        now = datetime.now()
        if type == "week":
            start_date = now - timedelta(weeks=1)
        elif type == "year":
            start_date = now - timedelta(days=365)
        else:  # default to month
            start_date = now - timedelta(days=30)

        # Get all invoices in the period
        response = supabase.table('invoices').select('*').gte('created_at', start_date.isoformat()).execute()
        invoices = response.data

        # Calculate totals and status counts
        total_amount = sum(float(inv.get('total', 0)) for inv in invoices)

        # Count by status
        status_counts = {}
        statuses = ['draft', 'pending', 'sent', 'paid', 'overdue', 'partially']

        for status_name in statuses:
            count = len([inv for inv in invoices if inv.get('status') == status_name])
            total_invoices = len(invoices) if invoices else 1
            percentage = round((count / total_invoices) * 100)
            status_counts[status_name] = percentage

        # Calculate unpaid amount
        unpaid_invoices = [inv for inv in invoices if inv.get('status') in ['unpaid', 'partially', 'overdue']]
        unpaid_amount = sum(float(inv.get('total', 0)) - float(inv.get('credit', 0)) for inv in unpaid_invoices)

        return {
            "success": True,
            "result": {
                "total": total_amount,
                "total_undue": unpaid_amount,
                "type": type,
                "performance": [
                    {"status": status, "percentage": status_counts.get(status, 0)}
                    for status in statuses
                ]
            },
            "message": f"Successfully get summary of invoices for the last {type}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/", response_model=Invoice)
async def create_invoice(
    invoice_data: InvoiceCreate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Create a new invoice"""
    try:
        invoice_dict = invoice_data.dict()
        invoice_dict['created_by'] = current_user['id']
        invoice_dict['status'] = 'draft'
        
        response = supabase.table('invoices').insert(invoice_dict).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create invoice"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Invoice])
async def get_invoices(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get all invoices"""
    try:
        query = supabase.table('invoices').select('*, customers(*)')
        
        if status:
            query = query.eq('status', status)
        
        if customer_id:
            query = query.eq('customer_id', customer_id)
        
        response = query.range(skip, skip + limit - 1).execute()
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{invoice_id}", response_model=Invoice)
async def get_invoice(
    invoice_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get a specific invoice"""
    try:
        response = supabase.table('invoices').select('*, customers(*)').eq('id', invoice_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{invoice_id}", response_model=Invoice)
async def update_invoice(
    invoice_id: int,
    invoice_update: InvoiceUpdate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update an invoice"""
    try:
        update_data = invoice_update.dict(exclude_unset=True)
        
        response = supabase.table('invoices').update(update_data).eq('id', invoice_id).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Delete an invoice"""
    try:
        response = supabase.table('invoices').delete().eq('id', invoice_id).execute()

        if response.data:
            return {"message": "Invoice deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



