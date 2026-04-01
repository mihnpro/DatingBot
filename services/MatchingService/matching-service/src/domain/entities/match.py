from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from src.domain.value_objects.status import MatchStatus


@dataclass
class Match:
    id: Optional[int]
    user1_id: int
    user2_id: int
    created_at: datetime
    status: MatchStatus

    def __init__(
        self,
        user1_id: int,
        user2_id: int,
        created_at: Optional[datetime] = None,
        status: Optional[MatchStatus] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.created_at = created_at or datetime.utcnow()
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'user1_id': self.user1_id,
            'user2_id': self.user2_id,
            'created_at': self.created_at.isoformat(),
            'status': self.status
        }
    def __post_init__(self):
        if self.user1_id > self.user2_id:
            self.user1_id, self.user2_id = self.user2_id, self.user1_id