"""Profile Domain Entity."""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum


class Gender(Enum):
    """Gender enumeration."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


@dataclass
class Profile:
    """
    Profile Entity.
    
    Represents user profile information for the dating platform.
    """
    user_id: int
    age: Optional[int] = None
    gender: Optional[Gender] = None
    city: Optional[str] = None
    interests: List[str] = field(default_factory=list)
    photos_count: int = 0
    fullness_percent: float = 0.0
    updated_at: datetime = field(default_factory=datetime.now(datetime.timezone.utc))
    id: Optional[int] = None
    
    # Field tracking for fullness calculation
    _fields: dict = field(default_factory=lambda: {
        "age": False,
        "gender": False,
        "city": False,
        "interests": False,
        "photos": False
    })
    
    def update(
        self,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        city: Optional[str] = None,
        interests: Optional[List[str]] = None
    ) -> None:
        """Update profile fields."""
        if age is not None:
            if not (18 <= age <= 100):
                raise ValueError("Age must be between 18 and 100")
            self.age = age
            self._fields["age"] = True
            
        if gender is not None:
            if gender not in [g.value for g in Gender]:
                raise ValueError(f"Gender must be one of: {[g.value for g in Gender]}")
            self.gender = Gender(gender)
            self._fields["gender"] = True
            
        if city is not None:
            self.city = city
            self._fields["city"] = True
            
        if interests is not None:
            self.interests = interests
            self._fields["interests"] = True
            
        self._calculate_fullness()
        self.updated_at = datetime.utcnow()
    
    def update_photos_count(self, count: int) -> None:
        """Update the number of photos."""
        self.photos_count = max(0, count)
        self._fields["photos"] = self.photos_count > 0
        self._calculate_fullness()
        self.updated_at = datetime.utcnow()
    
    def _calculate_fullness(self) -> None:
        """Calculate profile completeness percentage."""
        total_fields = len(self._fields)
        filled_fields = sum(1 for filled in self._fields.values() if filled)
        self.fullness_percent = (filled_fields / total_fields) * 100
    
    @property
    def is_complete(self) -> bool:
        """Check if profile is 100% complete."""
        return self.fullness_percent >= 100
    
    @property
    def is_minimal_complete(self) -> bool:
        """Check if profile has minimum required info."""
        return self._fields["gender"] and self._fields["age"]
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "age": self.age,
            "gender": self.gender.value if self.gender else None,
            "city": self.city,
            "interests": self.interests,
            "photos_count": self.photos_count,
            "fullness_percent": self.fullness_percent,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
