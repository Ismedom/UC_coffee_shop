from fastapi import FastAPI
from app.database import create_tables
from app.routers import api_router  
from app.middleware import APIAuthMiddleware, WebAuthMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(
    title="User Management API",
    description="A simple user management API with authentication",
    version="1.0.0"
)

app.add_middleware(APIAuthMiddleware)
app.add_middleware(WebAuthMiddleware)
app.add_middleware(SessionMiddleware, secret_key="hhoLbKYE2tkZcjlxy0DBJO0uxArpJscAnS4UmdGDydk")

app.include_router(api_router) 

@app.on_event("startup")
async def startup():
    """Create tables on startup (async)"""
    await create_tables()

@app.on_event("shutdown")
async def shutdown():
    """Nothing needed, AsyncSession handled by dependency"""
    pass