from pydantic import BaseModel
from datetime import datetime

class InteractionLikedEvent(BaseModel):
    event_type: str
    from_user_id: int
    to_user_id: int
    timestamp: datetime