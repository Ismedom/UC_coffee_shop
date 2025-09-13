from fastapi import APIRouter
from typing import List
from app.schemas import UserOut
# from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserOut])
async def get_users():
    """Get all users"""
    return 
    # await UserService.get_all_users()

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    """Get user by ID"""
    return 
    # await UserService.get_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: dict):
    """Update user information"""
    return 
# await UserService.update_user(user_id, user_data)

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete a user"""
    return 
    # await UserService.delete_user(user_id)