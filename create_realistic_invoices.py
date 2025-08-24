#!/usr/bin/env python3
"""
Create realistic sample invoices matching the design shown
"""
import asyncio
from datetime import datetime, timedelta
from app.core.database import get_supabase_service

async def create_realistic_invoices():
    """Create realistic sample invoices and customers"""
    try:
        supabase = get_supabase_service()
        
        # First, create some customers that match the design
        customers_to_create = [
            {"name": "muthu", "email": "muthu@example.com", "phone": "+1234567890"},
            {"name": "Lester Sible", "email": "lester@example.com", "phone": "+1234567891"},
            {"name": "Sheila Chambers", "email": "sheila@example.com", "phone": "+1234567892"},
            {"name": "test01-113", "email": "test01@example.com", "phone": "+1234567893"},
            {"name": "Tester Tester", "email": "tester@example.com", "phone": "+1234567894"},
            {"name": "PT MAJU MAKMUR", "email": "maju@example.com", "phone": "+1234567895"},
            {"name": "NewDemo", "email": "newdemo@example.com", "phone": "+1234567896"}
        ]
        
        # Insert customers
        customers_response = supabase.table('customers').insert(customers_to_create).execute()
        
        if not customers_response.data:
            print("❌ Failed to create customers")
            return
            
        customers = customers_response.data
        print(f"✅ Created {len(customers)} customers")
        
        # Clear existing invoices and payments
        supabase.table('payments').delete().neq('id', 0).execute()
        supabase.table('invoices').delete().neq('id', 0).execute()
        
        # Create realistic invoices matching the design
        realistic_invoices = [
            {
                "invoice_number": "25",
                "customer_id": customers[0]['id'],  # muthu
                "issue_date": "2025-03-27",
                "due_date": "2025-04-26",
                "total_amount": 11.322,
                "tax_amount": 1.03,
                "status": "sent",
                "notes": "Service invoice"
            },
            {
                "invoice_number": "26",
                "customer_id": customers[1]['id'],  # Lester Sible
                "issue_date": "2025-04-10",
                "due_date": "2025-05-10",
                "total_amount": 11019.272,
                "tax_amount": 1001.75,
                "status": "draft",
                "notes": "Project invoice"
            },
            {
                "invoice_number": "12",
                "customer_id": customers[2]['id'],  # Sheila Chambers
                "issue_date": "2025-01-13",
                "due_date": "2025-02-12",
                "total_amount": 47.00,
                "tax_amount": 4.27,
                "status": "pending",
                "notes": "Consultation"
            },
            {
                "invoice_number": "22",
                "customer_id": customers[3]['id'],  # test01-113
                "issue_date": "2025-02-20",
                "due_date": "2025-03-22",
                "total_amount": 303.614,
                "tax_amount": 27.60,
                "status": "draft",
                "notes": "Hardware"
            },
            {
                "invoice_number": "16",
                "customer_id": customers[4]['id'],  # Tester Tester
                "issue_date": "2025-02-02",
                "due_date": "2025-02-04",
                "total_amount": 33.278,
                "tax_amount": 3.03,
                "status": "sent",
                "notes": "Software license"
            },
            {
                "invoice_number": "11",
                "customer_id": customers[1]['id'],  # Lester Sible
                "issue_date": "2025-01-12",
                "due_date": "2025-02-11",
                "total_amount": 37.830,
                "tax_amount": 3.44,
                "status": "draft",
                "notes": "Maintenance"
            },
            {
                "invoice_number": "7",
                "customer_id": customers[5]['id'],  # PT MAJU MAKMUR
                "issue_date": "2024-12-11",
                "due_date": "2025-01-10",
                "total_amount": 966.00,
                "tax_amount": 87.82,
                "status": "draft",
                "notes": "Equipment"
            },
            {
                "invoice_number": "6",
                "customer_id": customers[5]['id'],  # PT MAJU MAKMUR
                "issue_date": "2024-12-03",
                "due_date": "2025-01-02",
                "total_amount": 4768.00,
                "tax_amount": 433.45,
                "status": "draft",
                "notes": "Services"
            },
            {
                "invoice_number": "9",
                "customer_id": customers[6]['id'],  # NewDemo
                "issue_date": "2024-12-27",
                "due_date": "2025-01-26",
                "total_amount": 51920.00,
                "tax_amount": 4720.00,
                "status": "pending",
                "notes": "Large project"
            },
            {
                "invoice_number": "21",
                "customer_id": customers[1]['id'],  # Lester Sible
                "issue_date": "2025-02-19",
                "due_date": "2025-03-21",
                "total_amount": 13.00,
                "tax_amount": 1.18,
                "status": "draft",
                "notes": "Small service"
            }
        ]
        
        # Insert invoices
        invoices_response = supabase.table('invoices').insert(realistic_invoices).execute()
        
        if not invoices_response.data:
            print("❌ Failed to create invoices")
            return
            
        invoices = invoices_response.data
        print(f"✅ Created {len(invoices)} invoices")
        
        # Create payments to match the design
        payments_to_create = [
            # Invoice 25 (muthu) - fully paid
            {
                "customer_id": customers[0]['id'],
                "invoice_id": invoices[0]['id'],
                "amount": 11.322,
                "payment_method": "Credit Card",
                "payment_date": "2025-03-28",
                "status": "completed"
            },
            # Invoice 12 (Sheila Chambers) - fully paid
            {
                "customer_id": customers[2]['id'],
                "invoice_id": invoices[2]['id'],
                "amount": 47.00,
                "payment_method": "Bank Transfer",
                "payment_date": "2025-01-15",
                "status": "completed"
            },
            # Invoice 22 (test01-113) - partially paid
            {
                "customer_id": customers[3]['id'],
                "invoice_id": invoices[3]['id'],
                "amount": 554.00,
                "payment_method": "Cash",
                "payment_date": "2025-02-25",
                "status": "completed"
            },
            # Invoice 6 (PT MAJU MAKMUR) - partially paid
            {
                "customer_id": customers[5]['id'],
                "invoice_id": invoices[7]['id'],
                "amount": 472.00,
                "payment_method": "Bank Transfer",
                "payment_date": "2024-12-10",
                "status": "completed"
            }
        ]
        
        # Insert payments
        payments_response = supabase.table('payments').insert(payments_to_create).execute()
        
        if payments_response.data:
            print(f"✅ Created {len(payments_response.data)} payments")
        else:
            print("❌ Failed to create payments")
            
        print("✅ Realistic sample data created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating realistic data: {e}")

if __name__ == "__main__":
    asyncio.run(create_realistic_invoices())
