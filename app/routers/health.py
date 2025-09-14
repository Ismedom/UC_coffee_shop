from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "user-api",
        "version": "1.0.0"
    }