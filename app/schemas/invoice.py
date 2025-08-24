from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


class InvoiceItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int
    unit_price: Decimal
    total_price: Decimal


class InvoiceBase(BaseModel):
    customer_id: int
    invoice_number: Optional[str] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    total_amount: Decimal
    tax_amount: Optional[Decimal] = 0
    discount_amount: Optional[Decimal] = 0
    items: Optional[List[dict]] = []
    notes: Optional[str] = None
    terms: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    customer_id: Optional[int] = None
    invoice_number: Optional[str] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    total_amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    items: Optional[List[dict]] = None
    notes: Optional[str] = None
    terms: Optional[str] = None
    status: Optional[str] = None


class Invoice(InvoiceBase):
    id: int
    status: str  # draft, sent, paid, overdue, cancelled
    created_by: UUID
    quote_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
