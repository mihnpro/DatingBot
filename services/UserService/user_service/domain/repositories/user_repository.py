from __future__ import annotations

from typing import Optional, Protocol

from user_service.domain.entities.user import User


class UserRepository(Protocol):
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        raise NotImplementedError

    async def upsert_user(
        self,
        *,
        telegram_id: int,
        username: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
        referral_by_telegram_id: Optional[int],
    ) -> User:
        raise NotImplementedError

