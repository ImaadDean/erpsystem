from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


class QuoteBase(BaseModel):
    customer_id: int
    quote_number: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    total_amount: Decimal
    tax_amount: Optional[Decimal] = 0
    discount_amount: Optional[Decimal] = 0
    items: Optional[List[dict]] = []
    notes: Optional[str] = None
    terms: Optional[str] = None


class QuoteCreate(QuoteBase):
    pass


class QuoteUpdate(BaseModel):
    customer_id: Optional[int] = None
    quote_number: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    total_amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    items: Optional[List[dict]] = None
    notes: Optional[str] = None
    terms: Optional[str] = None
    status: Optional[str] = None


class Quote(QuoteBase):
    id: int
    status: str  # draft, sent, accepted, rejected, expired, converted
    created_by: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
