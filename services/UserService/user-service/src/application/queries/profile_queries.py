from dataclasses import dataclass
from typing import Optional


@dataclass
class GetProfileByUserIdQuery:
    user_id: int


@dataclass
class ListProfilesQuery:
    gender: Optional[str] = None
    city: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    limit: int = 100
    offset: int = 0