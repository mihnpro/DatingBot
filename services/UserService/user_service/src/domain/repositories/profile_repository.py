from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from ..entities.profile import Profile


class ProfileRepository(ABC):
    @abstractmethod
    async def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """Get profile by ID"""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        """Get profile by user ID"""
        pass
    
    @abstractmethod
    async def create(self, profile: Profile) -> Profile:
        """Create new profile"""
        pass
    
    @abstractmethod
    async def update(self, profile: Profile) -> Profile:
        """Update existing profile"""
        pass
    
    @abstractmethod
    async def delete(self, profile_id: int) -> bool:
        """Delete profile"""
        pass
    
    @abstractmethod
    async def list_profiles(
        self,
        gender: Optional[str] = None,
        city: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[Profile], int]:
        """List profiles with filters and pagination, returns (profiles, total_count)"""
        pass