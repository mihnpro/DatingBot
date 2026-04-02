from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
from contextlib import asynccontextmanager

from .interfaces.api.v1 import user_router, profile_router
from .infrastructure.database.connection import db_manager
from .infrastructure.messaging.rabbitmq import rabbitmq_client
from .infrastructure.cache.redis_client import redis_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting up UserService...")
    
    # Initialize database
    await db_manager.initialize()
    logger.info("Database initialized")
    
    # Create tables if they don't exist
    await db_manager.create_tables()
    logger.info("Database tables created")
    
    # Initialize RabbitMQ
    await rabbitmq_client.connect()
    logger.info("RabbitMQ connected")
    
    # Initialize Redis
    await redis_client.connect()
    logger.info("Redis connected")
    
    yield
    
    # Shutdown
    logger.info("Shutting down UserService...")
    
    # Close database connection
    await db_manager.close()
    logger.info("Database connection closed")
    
    # Close RabbitMQ connection
    await rabbitmq_client.close()
    logger.info("RabbitMQ connection closed")
    
    # Close Redis connection
    await redis_client.close()
    logger.info("Redis connection closed")


# Create FastAPI app
app = FastAPI(
    title="User Service",
    description="User and Profile Management Microservice",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Include routers
app.include_router(user_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "user-service",
        "version": "1.0.0"
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    # Check database connection
    try:
        session = await db_manager.get_session()
        await session.execute("SELECT 1")
        await session.close()
        db_status = "ok"
    except Exception as e:
        logger.error(f"Database readiness check failed: {e}")
        db_status = "failed"
    
    # Check RabbitMQ connection
    try:
        if rabbitmq_client.connection and rabbitmq_client.connection.is_open:
            rmq_status = "ok"
        else:
            rmq_status = "failed"
    except Exception:
        rmq_status = "failed"
    
    # Check Redis connection
    try:
        if redis_client.client:
            await redis_client.client.ping()
            redis_status = "ok"
        else:
            redis_status = "failed"
    except Exception:
        redis_status = "failed"
    
    is_ready = all(status == "ok" for status in [db_status, rmq_status, redis_status])
    
    return {
        "ready": is_ready,
        "checks": {
            "database": db_status,
            "rabbitmq": rmq_status,
            "redis": redis_status
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )