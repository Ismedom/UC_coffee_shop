from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.payment import Payment
from app.schemas import PaymentCreate, PaymentUpdateStatus, PaymentOut, PaymentCreateAndComplete
from app.database import get_db

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create", response_model=PaymentOut)
async def create_payment(payment: PaymentCreate, db: AsyncSession = Depends(get_db)):
    new_payment = Payment(
        user_id=payment.user_id,
        order_id=payment.order_id,
        amount=payment.amount,
        currency=payment.currency,
        method=payment.method,
        status="pending"
    )
    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)
    return new_payment

@router.post("/complete", response_model=PaymentOut)
async def create_and_complete_payment(payment_data: PaymentCreateAndComplete, db: AsyncSession = Depends(get_db)):
    new_payment = Payment(
        user_id=payment_data.user_id,
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        currency=payment_data.currency,
        method=payment_data.method,
        status=payment_data.status,
    )
    
    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)
    
    return new_payment

@router.put("/{payment_id}/status", response_model=PaymentOut)
async def update_payment_status(payment_id: int, data: PaymentUpdateStatus, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = data.status
    await db.commit()
    await db.refresh(payment)
    return payment

@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/", response_model=list[PaymentOut])
async def list_payments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment))
    return result.scalars().all()
