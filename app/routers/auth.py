from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import UserCreate, TokenUserResponse, LoginUser
from app.services.user_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=TokenUserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    try:
        return await AuthService.register_user(user, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(user: LoginUser, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return token"""
    try:
        return await AuthService.login_user(user, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/test")
async def test():
    return {"status":"ok"}

@router.post("/logout")
async def logout():
    """Logout user"""
    pass