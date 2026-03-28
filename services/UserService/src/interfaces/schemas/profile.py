from pydantic import BaseModel, Field, ConfigDict, validator
from datetime import datetime
from typing import Optional, List
from ...domain.value_objects.gender import Gender
from ...domain.entities.profile import Profile as DomainProfile 


class ProfileBase(BaseModel):
    age: Optional[int] = Field(None, ge=18, le=100)
    gender: Optional[Gender] = None
    city: Optional[str] = Field(None, max_length=255)
    interests: Optional[List[str]] = Field(default=[], max_items=20)
    
    @validator('interests')
    def validate_interests(cls, v):
        if v:
            for interest in v:
                if len(interest) > 50:
                    raise ValueError("Each interest must be less than 50 characters")
        return v


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=18, le=100)
    gender: Optional[Gender] = None
    city: Optional[str] = Field(None, max_length=255)
    interests: Optional[List[str]] = Field(None, max_items=20)
    photos_count: Optional[int] = Field(None, ge=0)
    
    @validator('interests')
    def validate_interests(cls, v):
        if v:
            for interest in v:
                if len(interest) > 50:
                    raise ValueError("Each interest must be less than 50 characters")
        return v


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int]
    gender: Optional[Gender]
    city: Optional[str]
    interests: List[str]
    photos_count: int
    fullness_percent: float
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  

    @classmethod
    def from_domain(cls, profile: DomainProfile) -> "ProfileResponse":
        """Convert domain Profile to API response model."""
        interests_list = profile.interests.to_list() if hasattr(profile.interests, 'to_list') else []
        return cls(
            id=profile.id,
            user_id=profile.user_id,
            age=profile.age,
            gender=profile.gender,    
            city=profile.city,
            interests=interests_list,
            photos_count=getattr(profile, 'photos_count', 0),
            fullness_percent=profile.fullness_percent if hasattr(profile, 'fullness_percent') else 0.0,
            updated_at=profile.updated_at if hasattr(profile, 'updated_at') else datetime.utcnow()
        )


class ProfileListResponse(BaseModel):
    profiles: list[ProfileResponse]
    total: int
    limit: int
    offset: int