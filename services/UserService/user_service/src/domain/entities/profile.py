from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from ..value_objects.gender import Gender
from ..value_objects.interests import Interests


@dataclass
class Profile:
    id: Optional[int]
    user_id: int
    age: Optional[int]
    gender: Optional[Gender]
    city: Optional[str]
    interests: Interests
    photos_count: int
    fullness_percent: float
    updated_at: datetime
    
    def __init__(
        self,
        user_id: int,
        age: Optional[int] = None,
        gender: Optional[Gender] = None,
        city: Optional[str] = None,
        interests: Optional[List[str]] = None,
        photos_count: int = 0,
        id: Optional[int] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.city = city
        self.interests = Interests(interests or [])
        self.photos_count = photos_count
        self.fullness_percent = self._calculate_fullness()
        self.updated_at = updated_at or datetime.utcnow()
    
    def _calculate_fullness(self) -> float:
        """Calculate profile completeness percentage"""
        fields = [
            self.age is not None,
            self.gender is not None,
            self.city is not None and len(self.city) > 0,
            len(self.interests) > 0,
            self.photos_count > 0
        ]
        
        filled = sum(fields)
        return (filled / len(fields)) * 100
    
    def update(
        self,
        age: Optional[int] = None,
        gender: Optional[Gender] = None,
        city: Optional[str] = None,
        interests: Optional[List[str]] = None,
        photos_count: Optional[int] = None
    ):
        """Update profile fields and recalculate fullness"""
        if age is not None:
            if age < 18 or age > 100:
                raise ValueError("Age must be between 18 and 100")
            self.age = age
        
        if gender is not None:
            self.gender = gender
        
        if city is not None:
            self.city = city
        
        if interests is not None:
            self.interests = Interests(interests)
        
        if photos_count is not None:
            self.photos_count = photos_count
        
        self.fullness_percent = self._calculate_fullness()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'age': self.age,
            'gender': str(self.gender) if self.gender else None,
            'city': self.city,
            'interests': self.interests.to_list(),
            'photos_count': self.photos_count,
            'fullness_percent': self.fullness_percent,
            'updated_at': self.updated_at.isoformat()
        }