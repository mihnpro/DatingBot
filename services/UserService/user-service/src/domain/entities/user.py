from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class User:
    id: Optional[int]
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    registered_at: datetime
    last_active: datetime
    referral_by: Optional[int]
    
    def __init__(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        referral_by: Optional[int] = None,
        id: Optional[int] = None,
        registered_at: Optional[datetime] = None,
        last_active: Optional[datetime] = None
    ):
        self.id = id
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.registered_at = registered_at or datetime.utcnow()
        self.last_active = last_active or datetime.utcnow()
        self.referral_by = referral_by
    
    def update_activity(self):
        """Update last active timestamp"""
        self.last_active = datetime.utcnow()
    
    def update_info(self, username: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None):
        """Update user information"""
        if username is not None:
            self.username = username
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        self.update_activity()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'registered_at': self.registered_at.isoformat(),
            'last_active': self.last_active.isoformat(),
            'referral_by': self.referral_by
        }