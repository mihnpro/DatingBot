from dataclasses import dataclass
from typing import Optional, List
from ...domain.value_objects.gender import Gender


@dataclass
class CreateProfileCommand:
    user_id: int
    age: Optional[int] = None
    gender: Optional[Gender] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None


@dataclass
class UpdateProfileCommand:
    user_id: int
    age: Optional[int] = None
    gender: Optional[Gender] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None
    photos_count: Optional[int] = None


@dataclass
class DeleteProfileCommand:
    user_id: int