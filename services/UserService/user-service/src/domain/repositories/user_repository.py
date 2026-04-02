from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        pass

    @abstractmethod
    async def get_by_telegram_username(self, username: str) -> Optional[User]:
        """Get user by Telegram username"""
        pass

    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create new user"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        pass
    
    @abstractmethod
    async def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """List users with pagination"""
        pass
    
    @abstractmethod
    async def get_referrals(self, user_id: int) -> List[User]:
        """Get users referred by this user"""
        pass