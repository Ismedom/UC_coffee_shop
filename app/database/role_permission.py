import asyncio
from app.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Role, Permission
from sqlalchemy import select
from app.database.connection import create_tables
from app.constants import permissions_data, roles_data

async def seed_data(session: AsyncSession):
    for perm_data in permissions_data:
        result = await session.execute(select(Permission).where(Permission.name == perm_data["name"]))
        if not result.scalar_one_or_none():
            perm = Permission(
                name=perm_data["name"],
                resource=perm_data["resource"],
                action=perm_data["action"]
            )
            session.add(perm)

    for role_data in roles_data:
        result = await session.execute(select(Role).where(Role.name == role_data["name"]))
        if not result.scalar_one_or_none():
            role = Role(
                name=role_data["name"],
                description=role_data["description"]
            )
            session.add(role)
    
    await session.commit()
    print("✅ Seeded roles and permissions!")

async def main():
    await create_tables()

    async with AsyncSessionLocal() as session:
        await seed_data(session)

if __name__ == "__main__":
    asyncio.run(main())