import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:123@localhost/pyhon1")
    
    @property
    def sync_database_url(self) -> str:
        """Convert async URL to sync for SQLAlchemy operations"""
        return self.DATABASE_URL.replace("+asyncpg", "")

settings = Settings()