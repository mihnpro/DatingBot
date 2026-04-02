from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from ....application.commands.profile_commands import CreateProfileCommand, UpdateProfileCommand, DeleteProfileCommand
from ....application.queries.profile_queries import GetProfileByUserIdQuery, ListProfilesQuery
from ....application.handlers.profile_handlers import ProfileHandlers
from ...schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse, ProfileListResponse
from ..dependencies import get_profile_handlers
from ....domain.value_objects.gender import Gender

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    handlers: ProfileHandlers = Depends(get_profile_handlers)
):
    """Create a new profile"""
    try:
        command = CreateProfileCommand(
            user_id=profile_data.user_id,
            age=profile_data.age,
            gender=profile_data.gender,
            city=profile_data.city,
            interests=profile_data.interests
        )
        profile = await handlers.create_profile(command)
        return ProfileResponse.from_domain(profile)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/user/{user_id}", response_model=ProfileResponse)
async def get_profile_by_user_id(
    user_id: int,
    handlers: ProfileHandlers = Depends(get_profile_handlers)
):
    """Get profile by user ID"""
    query = GetProfileByUserIdQuery(user_id=user_id)
    profile = await handlers.get_profile_by_user_id(query)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return ProfileResponse.from_domain(profile)


@router.put("/user/{user_id}", response_model=ProfileResponse)
async def update_profile(
    user_id: int,
    profile_data: ProfileUpdate,
    handlers: ProfileHandlers = Depends(get_profile_handlers)
):
    """Update profile"""
    try:
        command = UpdateProfileCommand(
            user_id=user_id,
            age=profile_data.age,
            gender=profile_data.gender,
            city=profile_data.city,
            interests=profile_data.interests,
            photos_count=profile_data.photos_count
        )
        profile = await handlers.update_profile(command)
        return ProfileResponse.from_domain(profile)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    user_id: int,
    handlers: ProfileHandlers = Depends(get_profile_handlers)
):
    """Delete profile"""
    command = DeleteProfileCommand(user_id=user_id)
    deleted = await handlers.delete_profile(command)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


@router.get("/", response_model=ProfileListResponse)
async def list_profiles(
    gender: Optional[str] = Query(None, description="Filter by gender"),
    city: Optional[str] = Query(None, description="Filter by city"),
    min_age: Optional[int] = Query(None, ge=18, le=100, description="Minimum age"),
    max_age: Optional[int] = Query(None, ge=18, le=100, description="Maximum age"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    handlers: ProfileHandlers = Depends(get_profile_handlers)
):
    """List profiles with filters and pagination"""
    query = ListProfilesQuery(
        gender=gender,
        city=city,
        min_age=min_age,
        max_age=max_age,
        limit=limit,
        offset=offset
    )
    profiles, total = await handlers.list_profiles(query)
    return ProfileListResponse(
        profiles=profiles,
        total=total,
        limit=limit,
        offset=offset
    )