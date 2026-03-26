from typing import List, Set


class Interests:
    def __init__(self, interests: List[str]):
        self._interests = self._validate_and_normalize(interests)
    
    @staticmethod
    def _validate_and_normalize(interests: List[str]) -> Set[str]:
        if not interests:
            return set()
        
        normalized = {interest.strip().lower() for interest in interests if interest and interest.strip()}
        
        if len(normalized) > 20:
            raise ValueError("Maximum 20 interests allowed")
        
        for interest in normalized:
            if len(interest) > 50:
                raise ValueError("Each interest must be less than 50 characters")
        
        return normalized
    
    def to_list(self) -> List[str]:
        return sorted(list(self._interests))
    
    def add(self, interest: str):
        new_interests = self._interests | {interest.strip().lower()}
        self._interests = self._validate_and_normalize(list(new_interests))
    
    def remove(self, interest: str):
        self._interests.discard(interest.strip().lower())
    
    def contains(self, interest: str) -> bool:
        return interest.strip().lower() in self._interests
    
    def __len__(self) -> int:
        return len(self._interests)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Interests):
            return False
        return self._interests == other._interests