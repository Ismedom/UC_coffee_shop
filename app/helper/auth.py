from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from app.schemas import CurrentUser
import jwt
from typing import Optional
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES =settings.ACCESS_TOKEN_EXPIRE_MINUTES

security = HTTPBearer()

def create_access_token(user_id: int, username: str, expires_delta: Optional[timedelta] = None):
    """Create JWT token with user_id and username"""
    to_encode = {
        "sub": str(user_id),
        "username": username,
        "iat": datetime.utcnow()
    }
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CurrentUser:
    """Decode JWT token and return user data"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        
        if user_id is None or username is None:
            raise credentials_exception
            
        return CurrentUser(user_id=int(user_id), username=username)
        
    except jwt.PyJWTError:
        raise credentials_exception