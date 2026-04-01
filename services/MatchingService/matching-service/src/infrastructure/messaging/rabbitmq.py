import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractExchange
import json
from typing import Callable, Awaitable
from datetime import datetime, timezone 

class RabbitMQClient:
    def __init__(self, url: str):
        self.url = url
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None
        self.exchange: AbstractExchange | None = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            "dating.events", aio_pika.ExchangeType.TOPIC, durable=True
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def publish_match_created(self, user1_id: int, user2_id: int, match_id: int):
        message = {
            "event_type": "match.created",
            "user1_id": user1_id,
            "user2_id": user2_id,
            "match_id": match_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key="match.created",
        )

    async def consume_likes(self, callback: Callable[[dict], Awaitable[None]]):
        queue = await self.channel.declare_queue("matching_service_likes", durable=True)
        await queue.bind(self.exchange, routing_key="interaction.liked")
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        body = json.loads(message.body.decode())
                        await callback(body)
                    except Exception as e:
                        print(f"Error processing message: {e}")