"""This module provides health check service for the backend."""

from fastapi import Response
from fastapi import status
from sqlalchemy import exc
from sqlalchemy import text

from utils.dependency.initialization import db_dep
from utils.logging.logger import logging

from . import model


def is_server_running(response: Response) -> model.RunningResponse:
    """Check if the service is running.

    Returns:
        RunningResponse: The running status of the service.
    """
    response.status_code = status.HTTP_200_OK
    return model.RunningResponse(status="pass")


def is_server_ready(db: db_dep, response: Response) -> model.ReadyResponse:
    """Check if the service is ready to handle requests (DB connection).

    Args:
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        ReadyResponse: The readiness status.
    """
    health_details = {"database": "unknown"}
    try:
        db.execute(text("SELECT 1"))
        health_details["database"] = "pass"
        overall_status = "pass"
        response.status_code = status.HTTP_200_OK
    except (exc.OperationalError, exc.DatabaseError) as e:
        logging.error(f"Database readiness check failed: {e}")

        health_details["database"] = "fail"
        overall_status = "fail"
        # 503 indicates the server is temporarily unable to handle the request
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return model.ReadyResponse(status=overall_status, details=health_details)
