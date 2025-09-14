from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class PurchaseOrderDetailCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class PurchaseOrderDetailRead(PurchaseOrderDetailCreate):
    id: int
    subtotal: float

    class Config:
        orm_mode = True

class PurchaseOrderCreate(BaseModel):
    user_id: int
    details: List[PurchaseOrderDetailCreate]

class PurchaseOrderRead(BaseModel):
    id: int
    user_id: Optional[int]
    total_amount: float
    created_at: datetime
    details: List[PurchaseOrderDetailRead]

    class Config:
        orm_mode = True
