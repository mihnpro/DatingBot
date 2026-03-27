from typing import Optional, AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...infrastructure.database.connection import db_manager
from ...infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from ...infrastructure.database.repositories.profile_repository_impl import ProfileRepositoryImpl
from ...application.handlers.user_handlers import UserHandlers
from ...application.handlers.profile_handlers import ProfileHandlers




async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides a database session and handles commit/rollback."""
    session = await db_manager.get_session()
    try:
        yield session
        await session.commit()         
    except Exception:
        await session.rollback()        
        raise
    finally:
        await session.close()          

async def get_user_repository(session: AsyncSession = Depends(get_db_session)):
    """Dependency to get user repository"""
    return UserRepositoryImpl(session)


async def get_profile_repository(session: AsyncSession = Depends(get_db_session)):
    """Dependency to get profile repository"""
    return ProfileRepositoryImpl(session)


async def get_user_handlers(
    user_repo=Depends(get_user_repository)
) -> UserHandlers:
    """Dependency to get user handlers"""
    return UserHandlers(user_repo)


async def get_profile_handlers(
    profile_repo=Depends(get_profile_repository),
    user_repo=Depends(get_user_repository)
) -> ProfileHandlers:
    """Dependency to get profile handlers"""
    return ProfileHandlers(profile_repo, user_repo)