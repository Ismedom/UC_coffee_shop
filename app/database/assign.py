import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.user import Role, Permission
from app.helper.assign import assign_permissions_to_role
from app.constants import permissions_data, role_permissions_map

async def seed():
    async with AsyncSessionLocal() as session:
        for perm in permissions_data:
            result = await session.execute(select(Permission).where(Permission.name == perm["name"]))
            perm_obj = result.scalar_one_or_none()
            if not perm_obj:
                perm_obj = Permission(
                    name=perm["name"],
                    resource=perm["resource"],
                    action=perm["action"],
                    description=f"{perm['action']} {perm['resource']}"
                )
                session.add(perm_obj)
        await session.commit()

        for role_name in role_permissions_map.keys():
            result = await session.execute(select(Role).where(Role.name == role_name))
            role = result.scalar_one_or_none()
            if not role:
                role = Role(name=role_name, description=f"{role_name.capitalize()} role")
                session.add(role)
        await session.commit()

        for role_name, perm_names in role_permissions_map.items():
            await assign_permissions_to_role(
                role_name=role_name,
                permission_names=perm_names,
                db=session
            )

        print("Seeder completed!")

if __name__ == "__main__":
    asyncio.run(seed())
