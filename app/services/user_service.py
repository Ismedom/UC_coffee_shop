from fastapi import HTTPException, status
from sqlalchemy.future import select
from app.schemas import UserCreate, LoginUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, Role
from app.helper.auth import create_access_token
from app.utils.security import verify_password

class AuthService:
    @staticmethod
    async def register_user(user: UserCreate, db: AsyncSession):
        result = await db.execute(select(User).where((User.email == user.email)))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise ValueError("Username or email already exists")

        new_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=True
        )
        if user.role_names:
            result = await db.execute(
                select(Role).where(Role.name.in_(user.role_names))
            )
            roles = result.scalars().all()
            new_user.roles.extend(roles)

        access_token = create_access_token(new_user.id, new_user.username)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user, attribute_names=["roles"])
        return {
            "access_token": access_token,
            "user": new_user.to_dict(),
            "roles": [role.name for role in new_user.roles]
        }
    
    async def login_user(user: LoginUser, db: AsyncSession):
        result = await db.execute(select(User).where(User.email == user.email))
        db_user = result.scalar_one_or_none()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(db_user.id, db_user.username)
        return {
            "access_token": access_token,
            "user": db_user.to_dict()
        }
    async def log_out():
        """ logout """
        return