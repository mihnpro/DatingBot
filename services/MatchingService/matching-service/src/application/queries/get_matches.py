from dataclasses import dataclass
from typing import List
from src.domain.repositories.match_repository import MatchRepository

@dataclass
class GetMatchesQuery:
    user_id: int
    limit: int = 20
    offset: int = 0

@dataclass
class MatchesResult:
    matches: List[dict] 
    total: int

class GetMatchesHandler:
    def __init__(self, match_repo: MatchRepository):
        self.match_repo = match_repo

    async def handle(self, query: GetMatchesQuery) -> MatchesResult:
        matches = await self.match_repo.get_user_matches(
            query.user_id, query.limit, query.offset
        )
        total = await self.match_repo.count_user_matches(query.user_id)
        result_list = []
        for m in matches:
            matched_user_id = m.user2_id if m.user1_id == query.user_id else m.user1_id
            result_list.append({
                "match_id": m.id,
                "matched_user_id": matched_user_id,
                "created_at": m.created_at,
            })
        return MatchesResult(matches=result_list, total=total)