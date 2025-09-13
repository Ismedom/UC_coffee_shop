from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import settings

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
metadata = Base.metadata

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
