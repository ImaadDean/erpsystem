#!/usr/bin/env python3
"""
Create sample quotes (proforma invoices) matching the design shown
"""
import asyncio
from datetime import datetime, timedelta
from app.core.database import get_supabase_service

async def create_sample_quotes():
    """Create sample quotes matching the design"""
    try:
        supabase = get_supabase_service()
        
        # Get existing customers
        customers_response = supabase.table('customers').select('*').execute()
        
        if not customers_response.data:
            print("❌ No customers found. Please create customers first.")
            return
            
        customers = customers_response.data
        
        # Create a mapping of customer names to IDs
        customer_map = {}
        for customer in customers:
            customer_map[customer['name']] = customer['id']
        
        # Clear existing quotes
        supabase.table('quotes').delete().neq('id', 0).execute()
        
        # Create sample quotes matching the design
        sample_quotes = [
            {
                "quote_number": "10",
                "customer_id": customer_map.get("Lester Sible", customers[0]['id']),
                "issue_date": "2025-05-26",
                "expiry_date": "2025-06-25",
                "total_amount": 44.00,
                "tax_amount": 0.00,
                "status": "accepted",
                "notes": "Proforma invoice #10"
            },
            {
                "quote_number": "11",
                "customer_id": customer_map.get("Tester Tester", customers[0]['id']),
                "issue_date": "2025-06-30",
                "expiry_date": "2025-07-30",
                "total_amount": 196.00,
                "tax_amount": 16.00,
                "status": "pending",
                "notes": "Proforma invoice #11"
            },
            {
                "quote_number": "6",
                "customer_id": customer_map.get("Tester Tester", customers[0]['id']),
                "issue_date": "2025-03-24",
                "expiry_date": "2025-04-23",
                "total_amount": 418519.56,
                "tax_amount": 54589.50,
                "status": "draft",
                "notes": "Large project proforma"
            },
            {
                "quote_number": "9",
                "customer_id": customer_map.get("Tester Tester", customers[0]['id']),
                "issue_date": "2025-05-21",
                "expiry_date": "2025-06-20",
                "total_amount": 172500.00,
                "tax_amount": 22500.00,
                "status": "draft",
                "notes": "Medium project proforma"
            },
            {
                "quote_number": "1",
                "customer_id": customer_map.get("Lester Sible", customers[0]['id']),
                "issue_date": "2025-04-06",
                "expiry_date": "2025-05-06",
                "total_amount": 193.00,
                "tax_amount": 25.00,
                "status": "sent",
                "notes": "Service proforma"
            },
            {
                "quote_number": "5",
                "customer_id": customer_map.get("ravi das", customers[0]['id']),
                "issue_date": "2025-03-24",
                "expiry_date": "2025-04-23",
                "total_amount": 41.00,
                "tax_amount": 1.00,
                "status": "pending",
                "notes": "Small service proforma"
            },
            {
                "quote_number": "4",
                "customer_id": customer_map.get("PT MAJU MAKMUR", customers[0]['id']),
                "issue_date": "2024-11-09",
                "expiry_date": "2024-12-09",
                "total_amount": 11800.00,
                "tax_amount": 1800.00,
                "status": "declined",
                "notes": "Equipment proforma - declined"
            },
            {
                "quote_number": "4",  # Different quote with same number for different customer
                "customer_id": customer_map.get("Lester Sible", customers[0]['id']),
                "issue_date": "2024-11-09",
                "expiry_date": "2024-12-09",
                "total_amount": 345.00,
                "tax_amount": 45.00,
                "status": "accepted",
                "notes": "Service proforma - accepted"
            },
            {
                "quote_number": "3",
                "customer_id": customer_map.get("Lester Sible", customers[0]['id']),
                "issue_date": "2024-12-19",
                "expiry_date": "2025-01-18",
                "total_amount": 112.00,
                "tax_amount": 1.00,
                "status": "draft",
                "notes": "Consultation proforma"
            },
            {
                "quote_number": "8",
                "customer_id": customer_map.get("muthu", customers[0]['id']),
                "issue_date": "2025-05-09",
                "expiry_date": "2025-06-08",
                "total_amount": 3742.00,
                "tax_amount": 1312.00,
                "status": "draft",
                "notes": "Development proforma"
            }
        ]
        
        # If we don't have the specific customers, create them
        missing_customers = []
        for customer_name in ["ravi das"]:
            if customer_name not in customer_map:
                missing_customers.append({
                    "name": customer_name,
                    "email": f"{customer_name.replace(' ', '').lower()}@example.com",
                    "phone": "+1234567890"
                })
        
        if missing_customers:
            new_customers_response = supabase.table('customers').insert(missing_customers).execute()
            if new_customers_response.data:
                for customer in new_customers_response.data:
                    customer_map[customer['name']] = customer['id']
                print(f"✅ Created {len(new_customers_response.data)} missing customers")
        
        # Update customer IDs in quotes
        for quote in sample_quotes:
            customer_name = None
            for name, cust_id in customer_map.items():
                if cust_id == quote['customer_id']:
                    customer_name = name
                    break
            
            if customer_name and customer_name in customer_map:
                quote['customer_id'] = customer_map[customer_name]
        
        # Insert sample quotes
        quotes_response = supabase.table('quotes').insert(sample_quotes).execute()
        
        if quotes_response.data:
            print(f"✅ Created {len(quotes_response.data)} quotes")
            for quote in quotes_response.data:
                subtotal = float(quote['total_amount']) - float(quote['tax_amount'])
                print(f"   - Quote #{quote['quote_number']}: s{subtotal:.0f} subtotal, s{quote['total_amount']:.0f} total ({quote['status']})")
        else:
            print("❌ Failed to create quotes")
            
    except Exception as e:
        print(f"❌ Error creating sample quotes: {e}")

if __name__ == "__main__":
    asyncio.run(create_sample_quotes())
