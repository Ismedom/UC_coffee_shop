import asyncio
from sqlalchemy import select
from app.database.connection import AsyncSessionLocal, create_tables
from app.models import User, PurchaseOrder, Role, Permission, product

async def seed():
    await create_tables()

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        existing_user = result.first()
        if existing_user:
            print("Database already seeded!")
            return

        users = [
            User(username="admin", email="admin@example.com", password="12345678", is_active=True),
            # User(username="john", email="john@example.com", password="12345678", is_active=True),
        ]
        db.add_all(users)
        await db.commit()
        print("Database seeded!")

if __name__ == "__main__":
    asyncio.run(seed())
