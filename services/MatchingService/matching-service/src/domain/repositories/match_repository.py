from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.match import Match

class MatchRepository(ABC):
    @abstractmethod
    async def create(self, match: Match) -> Match:
        """Сохранить мэтч, вернуть с id"""
        pass

    @abstractmethod
    async def exists(self, user1_id: int, user2_id: int) -> bool:
        """Проверить существование мэтча между парой (канонический порядок)"""
        pass

    @abstractmethod
    async def get_user_matches(
        self, user_id: int, limit: int, offset: int
    ) -> List[Match]:
        """Получить мэтчи пользователя с пагинацией"""
        pass