"""User Domain Entity."""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class User:
    """
    User Aggregate Root.
    
    Represents a user in the system, identified by their Telegram account.
    """
    telegram_id: int
    username: Optional[str] = None
    first_name: str = ""
    last_name: Optional[str] = None
    registered_at: datetime = field(default_factory=datetime.now(datetime.timezone.utc))
    last_active: datetime = field(default_factory=datetime.now(datetime.timezone.utc))
    referral_by: Optional[int] = None
    id: Optional[int] = None
    
    def update_activity(self) -> None:
        """Update the last active timestamp."""
        self.last_active = datetime.now(datetime.timezone.utc)
    
    def update_profile(
        self,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> None:
        """Update user profile information."""
        if username is not None:
            self.username = username
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        self.update_activity()
    
    def set_referral(self, referrer_id: int) -> None:
        """Set the referral who invited this user."""
        if self.referral_by is None:
            self.referral_by = referrer_id
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    @property
    def display_name(self) -> str:
        """Get display name (username or full name)."""
        return f"@{self.username}" if self.username else self.full_name
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "registered_at": self.registered_at.isoformat() if self.registered_at else None,
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "referral_by": self.referral_by,
        }
