from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
import jwt
from app.config import settings

PUBLIC_ROUTES = [
    "/api/v1/auth/login", 
    "/api/v1/auth/register", 
    "/api/v1/auth/login-user"
]

PUBLIC_WEB_ROUTES = [
    "/",
    "/login",
    "/register",
    "/docs",
    "/redoc",
    "/openapi.json"
]

class APIAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        if request.url.path.startswith("/api"):
            if request.url.path in PUBLIC_ROUTES:
                return await call_next(request)
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse({"detail": "Missing or invalid token"}, status_code=401)

            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                request.state.user_id = payload.get("sub")
                request.state.username = payload.get("username")
            except jwt.PyJWTError:
                return JSONResponse({"detail": "Invalid token"}, status_code=401)

        return await call_next(request)


class WebAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/api") or path in PUBLIC_WEB_ROUTES:
            return await call_next(request)

        user_id = request.session.get("user_id")
        username = request.session.get("username")

        if not user_id:
            return RedirectResponse(url="/login", status_code=302)

        request.state.user_id = user_id
        request.state.username = username

        return await call_next(request)