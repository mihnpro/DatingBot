from typing import Optional
from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from ..commands.user_commands import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from ..queries.user_queries import GetUserByIdQuery, GetUserByTelegramIdQuery, ListUsersQuery, GetReferralsQuery


class UserHandlers:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def create_user(self, command: CreateUserCommand) -> User:
        """Handle create user command"""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_telegram_id(command.telegram_id)
        if existing_user:
            raise ValueError(f"User with telegram_id {command.telegram_id} already exists")
        
        # Create user entity
        user = User(
            telegram_id=command.telegram_id,
            username=command.username,
            first_name=command.first_name,
            last_name=command.last_name,
            referral_by=command.referral_by
        )
        
        # Save to repository
        return await self.user_repository.create(user)
    
    async def update_user(self, command: UpdateUserCommand) -> User:
        """Handle update user command"""
        user = await self.user_repository.get_by_id(command.user_id)
        if not user:
            raise ValueError(f"User with id {command.user_id} not found")
        
        user.update_info(
            username=command.username,
            first_name=command.first_name,
            last_name=command.last_name
        )
        
        return await self.user_repository.update(user)
    
    async def delete_user(self, command: DeleteUserCommand) -> bool:
        """Handle delete user command"""
        return await self.user_repository.delete(command.user_id)
    
    async def get_user_by_id(self, query: GetUserByIdQuery) -> Optional[User]:
        """Handle get user by id query"""
        return await self.user_repository.get_by_id(query.user_id)
    
    async def get_user_by_telegram_id(self, query: GetUserByTelegramIdQuery) -> Optional[User]:
        """Handle get user by telegram id query"""
        return await self.user_repository.get_by_telegram_id(query.telegram_id)
    
    async def list_users(self, query: ListUsersQuery) -> list:
        """Handle list users query"""
        return await self.user_repository.list_users(limit=query.limit, offset=query.offset)
    
    async def get_referrals(self, query: GetReferralsQuery) -> list:
        """Handle get referrals query"""
        user = await self.user_repository.get_by_id(query.user_id)
        if not user:
            raise ValueError(f"User with id {query.user_id} not found")
        
        return await self.user_repository.get_referrals(query.user_id)