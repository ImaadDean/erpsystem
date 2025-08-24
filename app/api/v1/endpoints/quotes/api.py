from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from supabase import Client
from app.core.database import get_supabase, get_supabase_service
from app.core.security import get_current_user
from app.schemas.quote import Quote, QuoteCreate, QuoteUpdate
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/summary")
async def get_quotes_summary(
    type: str = "month",
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_service)
):
    """Get quotes summary statistics"""
    try:
        # Calculate date range based on type
        now = datetime.now()
        if type == "week":
            start_date = now - timedelta(weeks=1)
        elif type == "year":
            start_date = now - timedelta(days=365)
        else:  # default to month
            start_date = now - timedelta(days=30)

        # Get all quotes in the period
        response = supabase.table('quotes').select('*').gte('created_at', start_date.isoformat()).execute()
        quotes = response.data

        # Calculate totals and status counts
        total_amount = sum(float(quote.get('total', 0)) for quote in quotes)

        # Count by status
        status_counts = {}
        statuses = ['draft', 'pending', 'sent', 'accepted', 'declined', 'expired']

        for status_name in statuses:
            count = len([quote for quote in quotes if quote.get('status') == status_name])
            total_quotes = len(quotes) if quotes else 1
            percentage = round((count / total_quotes) * 100)
            status_counts[status_name] = percentage

        return {
            "success": True,
            "result": {
                "total": total_amount,
                "type": type,
                "performance": [
                    {"status": status, "percentage": status_counts.get(status, 0)}
                    for status in statuses
                ]
            },
            "message": f"Successfully get summary of quotes for the last {type}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/", response_model=Quote)
async def create_quote(
    quote_data: QuoteCreate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Create a new quote"""
    try:
        quote_dict = quote_data.dict()
        quote_dict['created_by'] = current_user['id']
        quote_dict['status'] = 'draft'
        
        response = supabase.table('quotes').insert(quote_dict).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create quote"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Quote])
async def get_quotes(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get all quotes"""
    try:
        query = supabase.table('quotes').select('*, customers(*)')
        
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


@router.get("/{quote_id}", response_model=Quote)
async def get_quote(
    quote_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get a specific quote"""
    try:
        response = supabase.table('quotes').select('*, customers(*)').eq('id', quote_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{quote_id}", response_model=Quote)
async def update_quote(
    quote_id: int,
    quote_update: QuoteUpdate,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update a quote"""
    try:
        update_data = quote_update.dict(exclude_unset=True)
        
        response = supabase.table('quotes').update(update_data).eq('id', quote_id).execute()
        
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{quote_id}/convert-to-invoice")
async def convert_quote_to_invoice(
    quote_id: int,
    current_user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Convert a quote to an invoice"""
    try:
        # Get the quote
        quote_response = supabase.table('quotes').select('*').eq('id', quote_id).execute()
        
        if not quote_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )
        
        quote = quote_response.data[0]
        
        # Create invoice from quote
        invoice_data = {
            'customer_id': quote['customer_id'],
            'quote_id': quote_id,
            'total_amount': quote['total_amount'],
            'tax_amount': quote.get('tax_amount', 0),
            'discount_amount': quote.get('discount_amount', 0),
            'items': quote.get('items', []),
            'notes': quote.get('notes', ''),
            'created_by': current_user['id'],
            'status': 'draft'
        }
        
        invoice_response = supabase.table('invoices').insert(invoice_data).execute()
        
        if invoice_response.data:
            # Update quote status to converted
            supabase.table('quotes').update({'status': 'converted'}).eq('id', quote_id).execute()
            
            return {
                "message": "Quote converted to invoice successfully",
                "invoice_id": invoice_response.data[0]['id']
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to convert quote to invoice"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



