from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role_names: Optional[List[str]] = None

class LoginUser(BaseModel):
    email: str
    password: str

class RoleBase(BaseModel):
    roles: Optional[List[str]] = None

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class TokenUserResponse(BaseModel):
    access_token: str
    user: UserOut
    roles: RoleBase

    class Config:
        from_attributes = True