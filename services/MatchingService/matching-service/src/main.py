import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.database.postgres import (
    create_async_engine, async_sessionmaker, PostgresMatchRepository, Base
)
from src.infrastructure.cache.redis import RedisClient
from src.infrastructure.messaging.rabbitmq import RabbitMQClient
from src.application.handlers.like_handler import LikeHandler
from src.application.queries.get_matches import GetMatchesHandler
from src.application.commands.process_like import ProcessLikeCommand
from src.interfaces.api.v1.router import router as api_router
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres_dsn = os.getenv("POSTGRES_DSN", "postgresql+asyncpg://user:pass@localhost/matching_db")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

    engine = create_async_engine(postgres_dsn, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    match_repo = PostgresMatchRepository(session_factory)

    redis_client = RedisClient(redis_url)
    await redis_client.connect()

    rabbitmq_client = RabbitMQClient(rabbitmq_url)
    await rabbitmq_client.connect()

    like_handler = LikeHandler(match_repo, redis_client, rabbitmq_client)
    get_matches_handler = GetMatchesHandler(match_repo)

    # Сохраняем в app.state для доступа из роутеров
    app.state.matches_handler = get_matches_handler
    app.state.redis = redis_client
    app.state.rabbitmq = rabbitmq_client

    async def consume_events():
        await rabbitmq_client.consume_likes(
            lambda event: like_handler.handle(
                ProcessLikeCommand(
                    from_user_id=event["from_user_id"],
                    to_user_id=event["to_user_id"]
                )
            )
        )
    asyncio.create_task(consume_events())

    yield

    await redis_client.close()
    await rabbitmq_client.close()
    await engine.dispose()

app = FastAPI(lifespan=lifespan, title="Matching Service")
app.include_router(api_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)