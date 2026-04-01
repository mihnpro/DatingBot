from fastapi import APIRouter, Depends, HTTPException, Request
from src.application.queries.get_matches import GetMatchesQuery, GetMatchesHandler
from src.interfaces.schemas.match import MatchesListResponse, MatchResponse

router = APIRouter(prefix="/v1", tags=["matches"])

def get_matches_handler(request: Request) -> GetMatchesHandler:
    return request.app.state.matches_handler

@router.get("/matches/{user_id}", response_model=MatchesListResponse)
async def get_user_matches(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    handler: GetMatchesHandler = Depends(get_matches_handler),
):
    query = GetMatchesQuery(user_id=user_id, limit=limit, offset=offset)
    result = await handler.handle(query)
    return MatchesListResponse(
        matches=[MatchResponse(**m) for m in result.matches],
        total=result.total
    )