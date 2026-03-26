from __future__ import annotations

from typing import Optional, Protocol

from user_service.domain.entities.profile import Profile


class ProfileRepository(Protocol):
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[Profile]:
        raise NotImplementedError

    async def upsert_profile(
        self,
        *,
        telegram_id: int,
        age: int | None,
        gender: str | None,
        city: Optional[str],
        interests: list[str] | None,
        photos_count: int | None,
        fullness_percent: float | None,
    ) -> Profile:
        raise NotImplementedError

