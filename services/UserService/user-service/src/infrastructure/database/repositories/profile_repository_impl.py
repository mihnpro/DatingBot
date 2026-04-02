from typing import Optional, List, Tuple
from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.entities.profile import Profile
from ....domain.repositories.profile_repository import ProfileRepository
from ....domain.value_objects.gender import Gender
from ..models import ProfileModel


class ProfileRepositoryImpl(ProfileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, model: ProfileModel) -> Profile:
        """Convert ORM model to domain entity"""
        gender = Gender.from_string(model.gender) if model.gender else None
        return Profile(
            id=model.id,
            user_id=model.user_id,
            age=model.age,
            gender=gender,
            city=model.city,
            interests=model.interests or [],
            photos_count=model.photos_count,
            updated_at=model.updated_at
        )
    
    def _to_model(self, profile: Profile) -> ProfileModel:
        """Convert domain entity to ORM model"""
        return ProfileModel(
            id=profile.id,
            user_id=profile.user_id,
            age=profile.age,
            gender=str(profile.gender) if profile.gender else None,
            city=profile.city,
            interests=profile.interests.to_list() if profile.interests else [],
            photos_count=profile.photos_count,
            fullness_percent=profile.fullness_percent,
            updated_at=profile.updated_at
        )
    
    async def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """Get profile by ID"""
        result = await self.session.execute(
            select(ProfileModel).where(ProfileModel.id == profile_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        """Get profile by user ID"""
        result = await self.session.execute(
            select(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def create(self, profile: Profile) -> Profile:
        """Create new profile"""
        model = self._to_model(profile)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, profile: Profile) -> Profile:
        """Update existing profile"""
        await self.session.execute(
            update(ProfileModel)
            .where(ProfileModel.user_id == profile.user_id)
            .values(
                age=profile.age,
                gender=str(profile.gender) if profile.gender else None,
                city=profile.city,
                interests=profile.interests.to_list(),
                photos_count=profile.photos_count,
                fullness_percent=profile.fullness_percent,
                updated_at=profile.updated_at
            )
        )
        await self.session.flush()
        
        # Fetch updated profile
        return await self.get_by_user_id(profile.user_id)
    
    async def delete(self, profile_id: int) -> bool:
        """Delete profile"""
        result = await self.session.execute(
            delete(ProfileModel).where(ProfileModel.id == profile_id)
        )
        await self.session.flush()
        return result.rowcount > 0
    
    async def list_profiles(
        self,
        gender: Optional[str] = None,
        city: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[Profile], int]:
        """List profiles with filters and pagination"""
        query = select(ProfileModel)
        count_query = select(func.count()).select_from(ProfileModel)
        
        # Apply filters
        conditions = []
        if gender:
            conditions.append(ProfileModel.gender == gender)
        if city:
            conditions.append(ProfileModel.city == city)
        if min_age is not None:
            conditions.append(ProfileModel.age >= min_age)
        if max_age is not None:
            conditions.append(ProfileModel.age <= max_age)
        
        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))
        
        # Get total count
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()
        
        # Get paginated results
        query = query.order_by(ProfileModel.id).limit(limit).offset(offset)
        result = await self.session.execute(query)
        models = result.scalars().all()
        
        profiles = [self._to_domain(model) for model in models]
        return profiles, total