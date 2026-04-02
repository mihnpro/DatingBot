from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateUserCommand:
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    referral_by: Optional[int] = None


@dataclass
class UpdateUserCommand:
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass
class DeleteUserCommand:
    user_id: int