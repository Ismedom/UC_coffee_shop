from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PaymentCreate(BaseModel):
    user_id: int
    order_id: int
    amount: Decimal
    currency: str = "USD"
    method: str

class PaymentUpdateStatus(BaseModel):
    status: str

class PaymentCreateAndComplete(BaseModel):
    user_id: int
    order_id: int
    amount: Decimal
    currency: str = "USD"
    method: str
    status: str = "completed"

class PaymentOut(BaseModel):
    id: int
    user_id: int
    order_id: int
    amount: Decimal
    currency: str
    method: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
