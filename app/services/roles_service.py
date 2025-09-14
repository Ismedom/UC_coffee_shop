from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Role
from fastapi.responses import RedirectResponse

class AuthService:
    @staticmethod
    async def create_role(name: str, description: str, db: AsyncSession):
        # role_name = name.replace(" ", "")
    
        new_role = Role(name=name, description=description)
        db.add(new_role)
        await db.commit()
        await db.refresh(new_role)
        db.refresh(new_role)
        return RedirectResponse(url="/roles", status_code=303)