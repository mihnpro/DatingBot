from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.entities.user import User
from ....domain.repositories.user_repository import UserRepository
from ..models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: UserModel) -> User:
        """Convert ORM model to domain entity"""
        return User(
            id=model.id,
            telegram_id=model.telegram_id,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            registered_at=model.registered_at,
            last_active=model.last_active,
            referral_by=model.referral_by
        )
    
    def _to_model(self, user: User) -> UserModel:
        """Convert domain entity to ORM model"""
        return UserModel(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            registered_at=user.registered_at,
            last_active=user.last_active,
            referral_by=user.referral_by
        )
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def create(self, user: User) -> User:
        """Create new user"""
        model = self._to_model(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, user: User) -> User:
        """Update existing user"""
        await self.session.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                last_active=user.last_active
            )
        )
        await self.session.flush()
        
        # Fetch updated user
        return await self.get_by_id(user.id)
    
    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        result = await self.session.execute(
            delete(UserModel).where(UserModel.id == user_id)
        )
        await self.session.flush()
        return result.rowcount > 0
    
    async def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """List users with pagination"""
        result = await self.session.execute(
            select(UserModel)
            .order_by(UserModel.id)
            .limit(limit)
            .offset(offset)
        )
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
    
    async def get_referrals(self, user_id: int) -> List[User]:
        """Get users referred by this user"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.referral_by == user_id)
        )
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]