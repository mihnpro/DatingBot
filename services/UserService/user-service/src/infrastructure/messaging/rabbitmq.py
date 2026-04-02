import json
import logging
from typing import Optional
import aio_pika
from aio_pika import Message, Connection, Channel, Exchange
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

logger = logging.getLogger(__name__)


class RabbitMQClient:
    def __init__(self):
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractRobustChannel] = None
        self.exchange: Optional[Exchange] = None
        self.url: Optional[str] = None
    
    async def connect(self, url: Optional[str] = None):
        """Connect to RabbitMQ"""
        if not url:
            import os
            url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
        
        self.url = url
        self.connection = await aio_pika.connect_robust(url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            'user_events',
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        logger.info("Connected to RabbitMQ")
    
    async def close(self):
        """Close RabbitMQ connection"""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("Closed RabbitMQ connection")
    
    async def publish_event(self, event_type: str, data: dict):
        """Publish event to exchange"""
        if not self.exchange:
            raise RuntimeError("RabbitMQ not connected")
        
        message = Message(
            body=json.dumps(data).encode(),
            content_type='application/json',
            headers={'event_type': event_type}
        )
        
        routing_key = f"user.{event_type}"
        await self.exchange.publish(message, routing_key=routing_key)
        logger.info(f"Published event {event_type}: {data}")


# Global instance
rabbitmq_client = RabbitMQClient()