from fastapi import FastAPI, Request
from app.database import create_tables
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.middleware import AuthMiddleware
import os

app = FastAPI(
    title="User Management API",
    description="A simple user management API with authentication",
    version="1.0.0"
)

app.add_middleware(AuthMiddleware)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {"request": request, "status": "healthy", "version": "1.0.0"}
    )

@app.on_event("startup")
async def startup():
    """Create tables on startup (async)"""
    await create_tables()

@app.on_event("shutdown")
async def shutdown():
    """Nothing needed, AsyncSession handled by dependency"""
    pass