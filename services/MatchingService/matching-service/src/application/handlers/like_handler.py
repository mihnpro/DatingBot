from src.application.commands.process_like import ProcessLikeCommand
from src.domain.repositories.match_repository import MatchRepository
from src.infrastructure.cache.redis import RedisClient
from src.infrastructure.messaging.rabbitmq import RabbitMQClient
from src.domain.entities.match import Match
from src.domain.value_objects.status import MatchStatus
from datetime import datetime
import os

TTL = int(os.getenv("MATCH_TTL_SECONDS", 86400))

class LikeHandler:
    def __init__(
        self,
        match_repo: MatchRepository,
        redis_client: RedisClient,
        rabbitmq: RabbitMQClient,
    ):
        self.match_repo = match_repo
        self.redis = redis_client
        self.rabbitmq = rabbitmq

    async def handle(self, cmd: ProcessLikeCommand):
        from_id = cmd.from_user_id
        to_id = cmd.to_user_id

        u1, u2 = (from_id, to_id) if from_id < to_id else (to_id, from_id)

        if await self.match_repo.exists(u1, u2):
            return

        reverse_exists = await self.redis.set_like(from_id, to_id, TTL)

        if reverse_exists:
            match = Match(
                id=None,
                user1_id=u1,
                user2_id=u2,
                created_at=datetime.utcnow(),
                status=MatchStatus.ACTIVE,
            )
            created = await self.match_repo.create(match)
            await self.redis.delete_like(to_id, from_id)
            await self.rabbitmq.publish_match_created(created.user1_id, created.user2_id, created.id)