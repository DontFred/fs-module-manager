"""Service module for handling module-related API routes.

This module provides functions to interact with the database and handle
responses for module-related operations.
"""

from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from api.v0.routes.auth.model import Token
from db.model import Module
from utils.dependency.initialization import db_dep
from utils.logging.initialization import logger

from . import model


def get_all_modules(
    db: db_dep,
    response: Response,
    params: model.AllModulesQueryParams,
    user_token: Token,
) -> list[model.ModuleListResponse]:
    """Retrieve all modules from the database.

    Parameters
    ----------
    db : db_dep
        The database dependency for querying the modules.
    response : Response
        The HTTP response object.

    Returns:
    -------
    list[model.ModuleListResponse]
        A list of module response objects.

    Raises:
    ------
    HTTPException
        If an error occurs while retrieving modules.
    """
    try:
        modules = db.query(Module).all()
        response.status_code = status.HTTP_200_OK
        return [modules]
    except Exception as e:
        logger.error(f"Error retrieving modules: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving modules.",
        )
