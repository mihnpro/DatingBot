from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, DateTime, String, UniqueConstraint
from datetime import datetime
from src.domain.entities.match import Match
from src.domain.value_objects.status import MatchStatus
from src.domain.repositories.match_repository import MatchRepository
from typing import List

Base = declarative_base()

class MatchModel(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    user1_id = Column(BigInteger, nullable=False)
    user2_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default=MatchStatus.ACTIVE.value)

    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="unique_match"),
    )

class PostgresMatchRepository(MatchRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def create(self, match: Match) -> Match:
        async with self.session_factory() as session:
            model = MatchModel(
                user1_id=match.user1_id,
                user2_id=match.user2_id,
                status=match.status.value,
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            match.id = model.id
            match.created_at = model.created_at
            return match

    async def exists(self, user1_id: int, user2_id: int) -> bool:
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id
        async with self.session_factory() as session:
            result = await session.execute(
                select(MatchModel).where(
                    MatchModel.user1_id == user1_id,
                    MatchModel.user2_id == user2_id
                )
            )
            return result.scalar_one_or_none() is not None

    async def get_user_matches(self, user_id: int, limit: int, offset: int) -> List[Match]:
        async with self.session_factory() as session:
            stmt = select(MatchModel).where(
                (MatchModel.user1_id == user_id) | (MatchModel.user2_id == user_id)
            ).order_by(MatchModel.created_at.desc()).offset(offset).limit(limit)
            result = await session.execute(stmt)
            models = result.scalars().all()
            matches = []
            for m in models:
                matches.append(Match(
                    id=m.id,
                    user1_id=m.user1_id,
                    user2_id=m.user2_id,
                    created_at=m.created_at,
                    status=MatchStatus(m.status),
                ))
            return matches

    async def count_user_matches(self, user_id: int) -> int:
        async with self.session_factory() as session:
            stmt = select(func.count()).select_from(MatchModel).where(
                (MatchModel.user1_id == user_id) | (MatchModel.user2_id == user_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one()