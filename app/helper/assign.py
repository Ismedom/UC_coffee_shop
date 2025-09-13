from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import Role, Permission

async def assign_permissions_to_role(role_name: str, permission_names: list[str], db: AsyncSession):
    result = await db.execute(select(Role).where(Role.name == role_name))
    role = result.scalar_one_or_none()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist")

    result = await db.execute(select(Permission).where(Permission.name.in_(permission_names)))
    permissions = result.scalars().all()

    if not permissions:
        raise ValueError(f"No permissions found with names: {permission_names}")

    for perm in permissions:
        if perm not in role.permissions:
            role.permissions.append(perm)

    db.add(role)
    await db.commit()
    await db.refresh(role, attribute_names=["permissions"])  # async-safe

    return [perm.name for perm in role.permissions]


# await assign_permissions_to_role(
#     role_name="admin",
#     permission_names=["read_users", "write_users", "read_posts", "write_posts"],
#     db=session
# )
