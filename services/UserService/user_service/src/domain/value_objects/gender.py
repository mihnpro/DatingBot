from enum import Enum
from typing import Optional


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    
    @classmethod
    def from_string(cls, value: str) -> Optional['Gender']:
        try:
            return cls(value.lower())
        except ValueError:
            return None
    
    def __str__(self) -> str:
        return self.value