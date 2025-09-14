from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router  
from .health import router as health_router
from .web import router as web_router
from .order import router as order_router
from .product import router as product_router

api_router = APIRouter()

api_router.include_router(product_router, prefix="/api/v1")
api_router.include_router(order_router, prefix="/api/v1")
api_router.include_router(auth_router, prefix="/api/v1")
api_router.include_router(users_router, prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(web_router)