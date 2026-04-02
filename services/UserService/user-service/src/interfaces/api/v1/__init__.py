"""API v1 endpoints."""
from .user_router import router as user_router
from .profile_router import router as profile_router

__all__ = ["user_router", "profile_router"]