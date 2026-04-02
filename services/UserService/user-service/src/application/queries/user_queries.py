from dataclasses import dataclass
from typing import Optional


@dataclass
class GetUserByIdQuery:
    user_id: int


@dataclass
class GetUserByTelegramIdQuery:
    telegram_id: int


@dataclass
class ListUsersQuery:
    limit: int = 100
    offset: int = 0


@dataclass
class GetReferralsQuery:
    user_id: int