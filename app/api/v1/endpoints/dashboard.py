"""
Dashboard API endpoints for public access
"""
from fastapi import APIRouter, Depends
from supabase import Client
from app.core.database import get_supabase_service
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/summary")
async def get_dashboard_summary(
    type: str = "month",
    supabase: Client = Depends(get_supabase_service)
):
    """Get dashboard summary data without authentication for demo purposes"""
    try:
        # Calculate date range based on type
        now = datetime.now()
        if type == "week":
            start_date = now - timedelta(weeks=1)
        elif type == "year":
            start_date = now - timedelta(days=365)
        else:  # default to month
            start_date = now - timedelta(days=30)

        # Mock user for internal API calls
        mock_user = {"id": "admin", "email": "admin@admin.com"}

        # Import the summary functions
        from app.api.v1.endpoints.customers.api import get_customers_summary
        from app.api.v1.endpoints.invoices.api import get_invoices_summary
        from app.api.v1.endpoints.quotes.api import get_quotes_summary
        from app.api.v1.endpoints.payments.api import get_payments_summary

        # Fetch all summary data
        customers_data = await get_customers_summary(type=type, current_user=mock_user, supabase=supabase)
        invoices_data = await get_invoices_summary(type=type, current_user=mock_user, supabase=supabase)
        quotes_data = await get_quotes_summary(type=type, current_user=mock_user, supabase=supabase)
        payments_data = await get_payments_summary(type=type, current_user=mock_user, supabase=supabase)

        return {
            "success": True,
            "result": {
                "customers": customers_data.get("result", {}),
                "invoices": invoices_data.get("result", {}),
                "quotes": quotes_data.get("result", {}),
                "payments": payments_data.get("result", {})
            },
            "message": f"Successfully retrieved dashboard summary for the last {type}"
        }

    except Exception as e:
        print(f"Dashboard summary error: {e}")
        return {
            "success": False,
            "result": {
                "customers": {"new": 0, "active": 0},
                "invoices": {"total": 0, "total_undue": 0, "performance": []},
                "quotes": {"total": 0, "performance": []},
                "payments": {"count": 0, "total": 0}
            },
            "message": f"Error retrieving dashboard data: {str(e)}"
        }


@router.get("/customers/summary")
async def get_public_customers_summary(
    type: str = "month",
    supabase: Client = Depends(get_supabase_service)
):
    """Public customers summary endpoint"""
    try:
        mock_user = {"id": "admin", "email": "admin@admin.com"}
        from app.api.v1.endpoints.customers.api import get_customers_summary
        return await get_customers_summary(type=type, current_user=mock_user, supabase=supabase)
    except Exception as e:
        return {"success": False, "result": {"new": 0, "active": 0}, "message": str(e)}


@router.get("/invoices/summary")
async def get_public_invoices_summary(
    type: str = "month",
    supabase: Client = Depends(get_supabase_service)
):
    """Public invoices summary endpoint"""
    try:
        mock_user = {"id": "admin", "email": "admin@admin.com"}
        from app.api.v1.endpoints.invoices.api import get_invoices_summary
        return await get_invoices_summary(type=type, current_user=mock_user, supabase=supabase)
    except Exception as e:
        return {"success": False, "result": {"total": 0, "total_undue": 0, "performance": []}, "message": str(e)}


@router.get("/quotes/summary")
async def get_public_quotes_summary(
    type: str = "month",
    supabase: Client = Depends(get_supabase_service)
):
    """Public quotes summary endpoint"""
    try:
        mock_user = {"id": "admin", "email": "admin@admin.com"}
        from app.api.v1.endpoints.quotes.api import get_quotes_summary
        return await get_quotes_summary(type=type, current_user=mock_user, supabase=supabase)
    except Exception as e:
        return {"success": False, "result": {"total": 0, "performance": []}, "message": str(e)}


@router.get("/payments/summary")
async def get_public_payments_summary(
    type: str = "month",
    supabase: Client = Depends(get_supabase_service)
):
    """Public payments summary endpoint"""
    try:
        mock_user = {"id": "admin", "email": "admin@admin.com"}
        from app.api.v1.endpoints.payments.api import get_payments_summary
        return await get_payments_summary(type=type, current_user=mock_user, supabase=supabase)
    except Exception as e:
        return {"success": False, "result": {"count": 0, "total": 0}, "message": str(e)}


@router.get("/customers")
async def get_public_customers_list(
    skip: int = 0,
    limit: int = 100,
    supabase: Client = Depends(get_supabase_service)
):
    """Public customers list endpoint"""
    try:
        query = supabase.table('customers').select('*')
        response = query.range(skip, skip + limit - 1).execute()

        # Clean up the data to handle None values
        customers = []
        if response.data:
            for customer in response.data:
                # Ensure created_by is either a valid UUID string or None
                if customer.get('created_by') == '':
                    customer['created_by'] = None
                customers.append(customer)

        return customers
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return []


@router.get("/invoices")
async def get_public_invoices_list(
    skip: int = 0,
    limit: int = 100,
    supabase: Client = Depends(get_supabase_service)
):
    """Public invoices list endpoint with customer and payment information"""
    try:
        # Fetch invoices with customer information
        invoices_query = supabase.table('invoices').select('*, customers(name)').order('created_at', desc=True)
        invoices_response = invoices_query.range(skip, skip + limit - 1).execute()

        # Fetch payments to calculate paid amounts
        payments_query = supabase.table('payments').select('invoice_id, amount')
        payments_response = payments_query.execute()

        # Create a map of invoice_id to total paid amount
        payments_map = {}
        if payments_response.data:
            for payment in payments_response.data:
                invoice_id = payment['invoice_id']
                amount = float(payment['amount'] or 0)
                if invoice_id in payments_map:
                    payments_map[invoice_id] += amount
                else:
                    payments_map[invoice_id] = amount

        # Process invoices to add customer names and payment information
        invoices = []
        if invoices_response.data:
            for invoice in invoices_response.data:
                # Ensure created_by is either a valid UUID string or None
                if invoice.get('created_by') == '':
                    invoice['created_by'] = None

                # Add customer name
                customer_name = 'Unknown Client'
                if invoice.get('customers') and invoice['customers']:
                    customer_name = invoice['customers']['name']
                invoice['customer_name'] = customer_name

                # Add paid amount
                invoice_id = invoice['id']
                paid_amount = payments_map.get(invoice_id, 0)
                invoice['paid_amount'] = paid_amount

                # Remove the nested customers object to keep response clean
                if 'customers' in invoice:
                    del invoice['customers']

                invoices.append(invoice)

        return invoices
    except Exception as e:
        print(f"Error fetching invoices: {e}")
        return []


@router.get("/quotes")
async def get_public_quotes_list(
    skip: int = 0,
    limit: int = 100,
    supabase: Client = Depends(get_supabase_service)
):
    """Public quotes list endpoint with customer information"""
    try:
        # Fetch quotes with customer information
        quotes_query = supabase.table('quotes').select('*, customers(name)').order('created_at', desc=True)
        quotes_response = quotes_query.range(skip, skip + limit - 1).execute()

        # Process quotes to add customer names and calculate subtotal
        quotes = []
        if quotes_response.data:
            for quote in quotes_response.data:
                # Ensure created_by is either a valid UUID string or None
                if quote.get('created_by') == '':
                    quote['created_by'] = None

                # Add customer name
                customer_name = 'Unknown Client'
                if quote.get('customers') and quote['customers']:
                    customer_name = quote['customers']['name']
                quote['customer_name'] = customer_name

                # Calculate subtotal (total - tax)
                total_amount = float(quote.get('total_amount', 0))
                tax_amount = float(quote.get('tax_amount', 0))
                subtotal = total_amount - tax_amount
                quote['subtotal'] = subtotal

                # Remove the nested customers object to keep response clean
                if 'customers' in quote:
                    del quote['customers']

                quotes.append(quote)

        return quotes
    except Exception as e:
        print(f"Error fetching quotes: {e}")
        return []


@router.put("/customers/{customer_id}")
async def update_public_customer(
    customer_id: int,
    customer_data: dict,
    supabase: Client = Depends(get_supabase_service)
):
    """Public customer update endpoint"""
    try:
        # Clean the data before updating
        update_data = {
            "name": customer_data.get("name"),
            "email": customer_data.get("email"),
            "phone": customer_data.get("phone"),
            "city": customer_data.get("city"),
            "country": customer_data.get("country"),
            "state": customer_data.get("state"),
            "address": customer_data.get("address"),
            "notes": customer_data.get("notes"),
            "updated_at": "now()"
        }

        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}

        response = supabase.table('customers').update(update_data).eq('id', customer_id).execute()

        if response.data:
            return {
                "success": True,
                "message": "Customer updated successfully",
                "data": response.data[0]
            }
        else:
            return {
                "success": False,
                "message": "Customer not found or update failed"
            }

    except Exception as e:
        print(f"Error updating customer: {e}")
        return {
            "success": False,
            "message": f"Error updating customer: {str(e)}"
        }


@router.post("/customers")
async def create_public_customer(
    customer_data: dict,
    supabase: Client = Depends(get_supabase_service)
):
    """Public customer create endpoint"""
    try:
        # Prepare the data for insertion
        insert_data = {
            "name": customer_data.get("name"),
            "email": customer_data.get("email"),
            "phone": customer_data.get("phone"),
            "city": customer_data.get("city"),
            "country": customer_data.get("country"),
            "state": customer_data.get("state"),
            "address": customer_data.get("address"),
            "notes": customer_data.get("notes"),
            "created_at": "now()",
            "updated_at": "now()"
        }

        # Remove None values
        insert_data = {k: v for k, v in insert_data.items() if v is not None}

        response = supabase.table('customers').insert(insert_data).execute()

        if response.data:
            return {
                "success": True,
                "message": "Customer created successfully",
                "data": response.data[0]
            }
        else:
            return {
                "success": False,
                "message": "Customer creation failed"
            }

    except Exception as e:
        print(f"Error creating customer: {e}")
        return {
            "success": False,
            "message": f"Error creating customer: {str(e)}"
        }


@router.delete("/customers/{customer_id}")
async def delete_public_customer(
    customer_id: int,
    supabase: Client = Depends(get_supabase_service)
):
    """Public customer delete endpoint"""
    try:
        response = supabase.table('customers').delete().eq('id', customer_id).execute()

        return {
            "success": True,
            "message": "Customer deleted successfully"
        }

    except Exception as e:
        print(f"Error deleting customer: {e}")
        return {
            "success": False,
            "message": f"Error deleting customer: {str(e)}"
        }
