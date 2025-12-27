"""Controller module for the health check endpoint.

This module defines the API routes for checking the health status of the
service.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from sqlalchemy.orm import Session

from db.initialzation import get_db

from . import model
from . import service

router = APIRouter(prefix="/v0/health", tags=["System"])


@router.get("/running", response_model=model.RunningResponse)
def check_running(response: Response):
    """Health check endpoint to verify service is running."""
    return service.is_server_running(response)


@router.get("/ready", response_model=model.ReadyResponse)
def check_ready(response: Response, db: Session = Depends(get_db)):
    """Health check endpoint to verify external dependencies (Readiness).

    Checks database connectivity. Returns 503 if DB is unreachable.
    """
    return service.is_server_ready(db, response)
