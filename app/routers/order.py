from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.order import PurchaseOrderCreate, PurchaseOrderRead
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=PurchaseOrderRead)
async def create_order(order: PurchaseOrderCreate, db: AsyncSession = Depends(get_db)):
    return await OrderService.create_order(db, order)


@router.get("/", response_model=List[PurchaseOrderRead])
async def list_orders(db: AsyncSession = Depends(get_db)):
    return await OrderService.list_orders(db)


@router.get("/{order_id}", response_model=PurchaseOrderRead)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = OrderService.delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}
