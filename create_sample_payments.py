#!/usr/bin/env python3
"""
Create sample payments for invoices in the ERP system
"""
import asyncio
from datetime import datetime, timedelta
from app.core.database import get_supabase_service

async def create_sample_payments():
    """Create sample payments for existing invoices"""
    try:
        supabase = get_supabase_service()
        
        # Check if payments already exist
        existing_payments = supabase.table('payments').select('*').limit(1).execute()
        
        if existing_payments.data:
            print("✅ Sample payments already exist!")
            print(f"   Found {len(existing_payments.data)} existing payments")
            return
        
        # Get existing invoices to create payments for
        invoices = supabase.table('invoices').select('*').execute()
        
        if not invoices.data:
            print("❌ No invoices found. Please create invoices first.")
            return
        
        # Sample payment data
        sample_payments = []
        
        for i, invoice in enumerate(invoices.data[:3]):  # Create payments for first 3 invoices
            if i == 0:
                # Full payment for first invoice
                sample_payments.append({
                    "customer_id": invoice['customer_id'],
                    "invoice_id": invoice['id'],
                    "amount": float(invoice['total_amount']),
                    "payment_method": "Credit Card",
                    "payment_date": (datetime.now() - timedelta(days=5)).date().isoformat(),
                    "reference_number": f"PAY-{invoice['invoice_number']}-001",
                    "notes": f"Full payment for {invoice['invoice_number']}",
                    "status": "completed"
                })
            elif i == 1:
                # Partial payment for second invoice
                partial_amount = float(invoice['total_amount']) * 0.5
                sample_payments.append({
                    "customer_id": invoice['customer_id'],
                    "invoice_id": invoice['id'],
                    "amount": partial_amount,
                    "payment_method": "Bank Transfer",
                    "payment_date": (datetime.now() - timedelta(days=10)).date().isoformat(),
                    "reference_number": f"PAY-{invoice['invoice_number']}-001",
                    "notes": f"Partial payment for {invoice['invoice_number']}",
                    "status": "completed"
                })
            elif i == 2:
                # Full payment for third invoice
                sample_payments.append({
                    "customer_id": invoice['customer_id'],
                    "invoice_id": invoice['id'],
                    "amount": float(invoice['total_amount']),
                    "payment_method": "Cash",
                    "payment_date": (datetime.now() - timedelta(days=2)).date().isoformat(),
                    "reference_number": f"PAY-{invoice['invoice_number']}-001",
                    "notes": f"Full payment for {invoice['invoice_number']}",
                    "status": "completed"
                })
        
        # Insert sample payments
        if sample_payments:
            response = supabase.table('payments').insert(sample_payments).execute()
            
            if response.data:
                print("✅ Sample payments created successfully!")
                print(f"   Created {len(response.data)} payments:")
                for payment in response.data:
                    print(f"   - Invoice #{payment['invoice_id']}: ${payment['amount']:.2f} ({payment['payment_method']})")
            else:
                print("❌ Failed to create sample payments")
        else:
            print("❌ No payments to create")
            
    except Exception as e:
        print(f"❌ Error creating sample payments: {e}")

if __name__ == "__main__":
    asyncio.run(create_sample_payments())
