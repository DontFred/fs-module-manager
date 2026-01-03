"""Controller module for handling module-related API endpoints.

This module defines the API routes for managing modules, including retrieving
all modules with optional query parameters. It uses FastAPI for routing and
depends on the service layer for business logic.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from utils.dependency.initialization import db_dep
from utils.dependency.initialization import user_dep

from . import model
from . import service

router = APIRouter(prefix="/v0/modules", tags=["Modules"])


@router.get("/")
def get_all_modules(
    db: db_dep,
    user_token: user_dep,
    response: Response,
    params: model.AllModulesQueryParams = Depends(),
):
    """Retrieve all modules based on the provided query parameters.

    Parameters:
    ----------
    db : db_dep
        Database dependency for accessing the database.
    user_token : user_dep
        Dependency for user authentication and authorization.
    response : Response
        FastAPI Response object for setting response headers or status.
    params : model.AllModulesQueryParams
        Query parameters for filtering or paginating the modules.

    Returns:
    -------
    List[Dict]
        A list of modules retrieved from the service layer.
    """
    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.get_all_modules(db, response, params, user_token)
