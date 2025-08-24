#!/usr/bin/env python3
"""
Script to create sample invoices in the database
"""
import asyncio
from datetime import datetime, timedelta
from app.core.database import get_supabase_service

async def create_sample_invoices():
    """Create sample invoices in the database"""
    try:
        supabase = get_supabase_service()
        
        # Check if invoices already exist
        existing_invoices = supabase.table('invoices').select('*').limit(1).execute()
        
        if existing_invoices.data:
            print("✅ Sample invoices already exist!")
            print(f"   Found {len(existing_invoices.data)} existing invoices")
            return
        
        # Get existing customers to link invoices to
        customers = supabase.table('customers').select('*').limit(5).execute()
        
        if not customers.data:
            print("❌ No customers found. Please create customers first.")
            return
        
        # Sample invoice data (matching the actual database schema)
        sample_invoices = [
            {
                "invoice_number": "INV-001",
                "customer_id": customers.data[0]['id'],
                "issue_date": (datetime.now() - timedelta(days=30)).date().isoformat(),
                "due_date": (datetime.now() - timedelta(days=0)).date().isoformat(),
                "total_amount": 1245.42,
                "tax_amount": 113.22,
                "discount_amount": 0.00,
                "status": "sent",
                "notes": "Monthly service invoice",
                "items": [
                    {
                        "name": "Web Development Service",
                        "description": "Monthly website maintenance",
                        "quantity": 1,
                        "unit_price": 1132.20,
                        "total_price": 1132.20
                    }
                ]
            },
            {
                "invoice_number": "INV-002",
                "customer_id": customers.data[1]['id'] if len(customers.data) > 1 else customers.data[0]['id'],
                "issue_date": (datetime.now() - timedelta(days=20)).date().isoformat(),
                "due_date": (datetime.now() + timedelta(days=10)).date().isoformat(),
                "total_amount": 11019.27,
                "tax_amount": 1001.75,
                "discount_amount": 0.00,
                "status": "draft",
                "notes": "Project development invoice",
                "items": [
                    {
                        "name": "Custom Software Development",
                        "description": "Full-stack web application",
                        "quantity": 1,
                        "unit_price": 10017.52,
                        "total_price": 10017.52
                    }
                ]
            },
            {
                "invoice_number": "INV-003",
                "customer_id": customers.data[2]['id'] if len(customers.data) > 2 else customers.data[0]['id'],
                "issue_date": (datetime.now() - timedelta(days=45)).date().isoformat(),
                "due_date": (datetime.now() - timedelta(days=15)).date().isoformat(),
                "total_amount": 47.00,
                "tax_amount": 4.27,
                "discount_amount": 0.00,
                "status": "sent",
                "notes": "Consultation fee",
                "items": [
                    {
                        "name": "Business Consultation",
                        "description": "Strategic planning session",
                        "quantity": 1,
                        "unit_price": 42.73,
                        "total_price": 42.73
                    }
                ]
            },
            {
                "invoice_number": "INV-004",
                "customer_id": customers.data[0]['id'],
                "issue_date": (datetime.now() - timedelta(days=10)).date().isoformat(),
                "due_date": (datetime.now() + timedelta(days=20)).date().isoformat(),
                "total_amount": 304.14,
                "tax_amount": 27.65,
                "discount_amount": 0.00,
                "status": "sent",
                "notes": "Hardware purchase",
                "items": [
                    {
                        "name": "Computer Hardware",
                        "description": "Server components",
                        "quantity": 2,
                        "unit_price": 138.25,
                        "total_price": 276.49
                    }
                ]
            },
            {
                "invoice_number": "INV-005",
                "customer_id": customers.data[1]['id'] if len(customers.data) > 1 else customers.data[0]['id'],
                "issue_date": (datetime.now() - timedelta(days=5)).date().isoformat(),
                "due_date": (datetime.now() + timedelta(days=25)).date().isoformat(),
                "total_amount": 33.28,
                "tax_amount": 3.03,
                "discount_amount": 0.00,
                "status": "draft",
                "notes": "Software license",
                "items": [
                    {
                        "name": "Software License",
                        "description": "Annual subscription",
                        "quantity": 1,
                        "unit_price": 30.25,
                        "total_price": 30.25
                    }
                ]
            }
        ]
        
        # Insert sample invoices
        response = supabase.table('invoices').insert(sample_invoices).execute()
        
        if response.data:
            print("✅ Sample invoices created successfully!")
            print(f"   Created {len(response.data)} invoices:")
            for invoice in response.data:
                print(f"   - {invoice['invoice_number']}: ${invoice['total_amount']:.2f} ({invoice['status']})")
        else:
            print("❌ Failed to create sample invoices")
            
    except Exception as e:
        print(f"❌ Error creating sample invoices: {e}")

if __name__ == "__main__":
    asyncio.run(create_sample_invoices())
