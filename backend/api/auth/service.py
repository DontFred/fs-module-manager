"""This module provides utility functions for handling JWT tokens.

Functions:
- create_access_token: Generates a JWT access token with optional expiration.
"""

import os
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from db.model import Faculty
from db.model import User
from db.model import UserRole
from utils.dependency.initialization import argon2_hasher
from utils.dependency.initialization import db_dep
from utils.logging.initialization import logging

from . import model

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "please1change1me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 240)
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token.

    Parameters
    ----------
    data : dict
        The data to encode in the token.
    expires_delta : timedelta | None, optional
        The expiration time delta for the token. Defaults to 15 minutes.

    Returns:
    -------
    str
        The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def authenticate_for_token(
    db: db_dep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> model.Token:
    """Authenticate a user and generate a JWT token.

    Parameters
    ----------
    db : db_dep
        The database dependency for querying user data.
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()]
        The form data containing the username and password.

    Returns:
    -------
    model.Token
        A token object containing the access token and its type.

    Raises:
    ------
    HTTPException
        If the user does not exist, the password is incorrect, or a database
        error occurs.
    """
    try:
        user = db.query(User).filter(User.user_id == form_data.username).first()
    except Exception as e:
        logging.error(
            f"Database error while checking existing user before create: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred.",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user_id or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not argon2_hasher.verify(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user_id or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.role == UserRole.ADMIN and user.faculty == Faculty.ADMIN:
        scope = "admin"
    elif user.role == UserRole.DEANERY and user.faculty == Faculty.ADMIN:
        scope = "deanery"
    elif (
        user.role == UserRole.EXAMINATION_OFFICE
        and user.faculty == Faculty.ADMIN
    ):
        scope = "examination_office"
    else:
        scope = f"{user.faculty.value.lower()[:2]}:{user.role.value.lower()}"
    access_token = create_access_token(
        data={"id": user.user_id, "name": user.name, "scope": scope},
        expires_delta=access_token_expires,
    )
    return model.Token(access_token=access_token, token_type="bearer")
