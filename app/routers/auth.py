from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from app.schemas import UserCreate, TokenUserResponse, LoginUser
from app.services.user_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(prefix="/auth", tags=["authentication"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

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

@router.post("/login-user")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Login like Laravel (set session cookie)"""
    try:
        user = await AuthService.login_user_from_web(email, password, db)
        if not user:
            return templates.TemplateResponse(
                "login.html", 
                {"request": request, "error": "Invalid credentials"}
            )
        request.session["user_id"] = user.id
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

    except ValueError as e:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": str(e)}
        )


@router.post("/test")
async def test():
    return {"status":"ok"}

@router.post("/logout")
async def logout():
    """Logout user"""
    pass