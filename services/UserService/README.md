# User Service

User and Profile Management Microservice with DDD architecture based on FastAPI.

## Features

- User management with Telegram integration
- Profile management with completeness scoring
- DDD (Domain-Driven Design) architecture
- Async support with FastAPI
- PostgreSQL database with SQLAlchemy
- Redis caching
- RabbitMQ event publishing
- Docker support

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd user-service

# Start with Docker
docker compose up

# Or run locally
uv venv
source .venv/bin/activate
uv pip install -e .
uvicorn src.main:app --reload