from fastapi import APIRouter, Depends
from app.models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy import select

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
async def get_products(db: AsyncSession = Depends(get_db)):
    """Get all products"""
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return products