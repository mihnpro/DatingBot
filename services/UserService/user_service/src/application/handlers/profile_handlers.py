from typing import Optional, Tuple, List
from ...domain.entities.profile import Profile
from ...domain.repositories.profile_repository import ProfileRepository
from ...domain.repositories.user_repository import UserRepository
from ..commands.profile_commands import CreateProfileCommand, UpdateProfileCommand, DeleteProfileCommand
from ..queries.profile_queries import GetProfileByUserIdQuery, ListProfilesQuery


class ProfileHandlers:
    def __init__(self, profile_repository: ProfileRepository, user_repository: UserRepository):
        self.profile_repository = profile_repository
        self.user_repository = user_repository
    
    async def create_profile(self, command: CreateProfileCommand) -> Profile:
        """Handle create profile command"""
        user = await self.user_repository.get_by_id(command.user_id)
        if not user:
            raise ValueError(f"User with id {command.user_id} not found")
        
        existing_profile = await self.profile_repository.get_by_user_id(command.user_id)
        if existing_profile:
            raise ValueError(f"Profile for user {command.user_id} already exists")
        
        profile = Profile(
            user_id=command.user_id,
            age=command.age,
            gender=command.gender,
            city=command.city,
            interests=command.interests
        )
        
        return await self.profile_repository.create(profile)
    
    async def update_profile(self, command: UpdateProfileCommand) -> Profile:
        """Handle update profile command"""
        profile = await self.profile_repository.get_by_user_id(command.user_id)
        if not profile:
            raise ValueError(f"Profile for user {command.user_id} not found")
        
        profile.update(
            age=command.age,
            gender=command.gender,
            city=command.city,
            interests=command.interests,
            photos_count=command.photos_count
        )
        
        return await self.profile_repository.update(profile)
    
    async def delete_profile(self, command: DeleteProfileCommand) -> bool:
        """Handle delete profile command"""
        profile = await self.profile_repository.get_by_user_id(command.user_id)
        if not profile:
            return False
        
        return await self.profile_repository.delete(profile.id)
    
    async def get_profile_by_user_id(self, query: GetProfileByUserIdQuery) -> Optional[Profile]:
        """Handle get profile by user id query"""
        return await self.profile_repository.get_by_user_id(query.user_id)
    
    async def list_profiles(self, query: ListProfilesQuery) -> Tuple[List[Profile], int]:
        """Handle list profiles query"""
        return await self.profile_repository.list_profiles(
            gender=query.gender,
            city=query.city,
            min_age=query.min_age,
            max_age=query.max_age,
            limit=query.limit,
            offset=query.offset
        )