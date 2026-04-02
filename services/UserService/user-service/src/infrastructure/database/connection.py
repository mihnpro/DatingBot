from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from typing import Optional
import os


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
    
    async def initialize(self, database_url: Optional[str] = None):
        """Initialize database connection"""
        if not database_url:
            database_url = os.getenv(
                'DATABASE_URL',
                'postgresql+asyncpg://user:password@localhost:5432/user_db'
            )
        
        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
            poolclass=NullPool
        )
        
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def close(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()
    
    async def get_session(self) -> AsyncSession:
        """Get database session"""
        if not self.async_session_maker:
            await self.initialize()
        return self.async_session_maker()
    
    async def create_tables(self):
        """Create all tables"""
        if not self.engine:
            await self.initialize()
        
        async with self.engine.begin() as conn:
            from .models import Base
            await conn.run_sync(Base.metadata.create_all)


# Global instance
db_manager = DatabaseManager()