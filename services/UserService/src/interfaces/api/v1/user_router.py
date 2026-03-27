from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ....application.commands.user_commands import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from ....application.queries.user_queries import GetUserByIdQuery, GetUserByTelegramIdQuery, ListUsersQuery, GetReferralsQuery
from ....application.handlers.user_handlers import UserHandlers
from ...schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from ..dependencies import get_user_handlers

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    handlers: UserHandlers = Depends(get_user_handlers)
):
    """Create a new user"""
    try:
        command = CreateUserCommand(
            telegram_id=user_data.telegram_id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            referral_by=user_data.referral_by
        )
        user = await handlers.create_user(command)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    handlers: UserHandlers = Depends(get_user_handlers)
):
    """Get user by ID"""
    query = GetUserByIdQuery(user_id=user_id)
    user = await handlers.get_user_by_id(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/telegram/{telegram_id}", response_model=UserResponse)
async def get_user_by_telegram_id(
    telegram_id: int,
    handlers: UserHandlers = Depends(get_user_handlers)
):
    """Get user by Telegram ID"""
    query = GetUserByTelegramIdQuery(telegram_id=telegram_id)
    user = await handlers.get_user_by_telegram_id(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    handlers: UserHandlers = Depends(get_user_handlers)
):
    """Update user"""
    try:
        command = UpdateUserCommand(
            user_id=user_id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        user = await handlers.update_user(command)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    handlers: UserHandlers = Depends(get_user_handlers)
):
    """Delete user"""
    command = DeleteUserCommand(user_id=user_id)
    deleted = await handlers.delete_user(command)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/", response_model=UserListResponse)
async def list_users(
    limit: int = 100,
    offset: int = 0,
    handlers: UserHandlers = Depends(get_user_handlers)
):
    """List users with pagination"""
    query = ListUsersQuery(limit=limit, offset=offset)
    users = await handlers.list_users(query)
    return UserListResponse(
        users=users,
        total=len(users),
        limit=limit,
        offset=offset
    )


@router.get("/{user_id}/referrals", response_model=List[UserResponse])
async def get_referrals(
    user_id: int,
    handlers: UserHandlers = Depends(get_user_handlers)
):
    """Get users referred by this user"""
    try:
        query = GetReferralsQuery(user_id=user_id)
        referrals = await handlers.get_referrals(query)
        return referrals
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))