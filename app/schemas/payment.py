from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


class PaymentBase(BaseModel):
    customer_id: int
    invoice_id: Optional[int] = None
    amount: Decimal
    payment_method: str  # cash, credit_card, bank_transfer, check, etc.
    payment_date: Optional[date] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    customer_id: Optional[int] = None
    invoice_id: Optional[int] = None
    amount: Optional[Decimal] = None
    payment_method: Optional[str] = None
    payment_date: Optional[date] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class Payment(PaymentBase):
    id: int
    status: str  # pending, completed, failed, cancelled
    created_by: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
