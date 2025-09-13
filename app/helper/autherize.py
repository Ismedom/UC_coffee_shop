from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.database import get_db

async def require_permission(user: User, perm_name: str, db: AsyncSession = Depends(get_db)):
    """
    Raises 403 if the user does not have the given permission.
    """
    perms = []
    for role in user.roles:
        perms.extend([p.name for p in role.permissions])

    if perm_name not in perms:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission '{perm_name}' required"
        )


# from functools import partial

# def permission_required(perm_name: str):
#     async def dependency(user: User = Depends(get_current_user)):
#         await require_permission(user, perm_name)
#     return Depends(dependency)

# @router.get("/users")
# async def read_users(_ = permission_required("read_users")):
#     return {"msg": "You have access"}