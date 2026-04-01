from pydantic import BaseModel
from datetime import datetime

class MatchResponse(BaseModel):
    match_id: int
    matched_user_id: int
    created_at: datetime

class MatchesListResponse(BaseModel):
    matches: list[MatchResponse]
    total: int