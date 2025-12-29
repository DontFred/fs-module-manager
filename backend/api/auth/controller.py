"""Authentication controller module.

This module defines the API routes and handlers for authentication-related
operations, such as obtaining access tokens.
"""

from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from utils.dependency.initialization import db_dep

from . import model
from . import service

router = APIRouter(prefix="/v0/auth", tags=["Authentication"])


@router.post("/token", response_model=model.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dep,
):
    """Handle user login and return an access token.

    Parameters
    ----------
    form_data : OAuth2PasswordRequestForm
        The form data containing username and password.
    db : db_dep
        The database dependency for accessing user data.

    Returns:
    -------
    model.Token
        A dictionary containing the access token and token type.
    """
    return await service.authenticate_for_token(db, form_data)
