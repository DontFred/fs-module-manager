"""This module provides the service configuration for the FastAPI application.

It includes:
- Middleware setup for CORS and rate limiting.
- Router registration for the application.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from api.v0.routes.health.controller import router as health_router
from api.v0.routes.users.controller import router as users_router

load_dotenv()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20/minute"],
    enabled=False if os.getenv("ENVIRONMENT") == "development" else True,
)


def register_api(app: FastAPI):
    """Register the router and configure middleware for API.

    It includes:
    - Middleware setup for CORS and rate limiting.
    - Router registration for the application.

    Parameters:
    ----------
    app : FastAPI
        The FastAPI application instance to which the router and middleware
        will be added.
    """
    frontend_port = int(os.getenv("FRONTEND_PORT", "3000"))
    origins = [
        f"http://localhost:{frontend_port}",
        f"http://127.0.0.1:{frontend_port}",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    app.include_router(health_router)
    app.include_router(users_router)
