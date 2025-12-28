"""Module for dependency initialization in the backend.

This module provides utility functions and dependencies for:
- Retrieving the current user based on an OAuth2 token.
- Managing database sessions.
- Configuring security contexts and JWT handling.
"""

import os
from typing import Annotated

from argon2 import PasswordHasher
from dotenv import load_dotenv
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session

from db.initialization import engine
from db.model import Faculty
from db.model import UserRole

load_dotenv()

ARGON_TIME_COST = int(os.getenv("ARGON_TIME_COST", 3))
ARGON_MEMORY_COST = int(os.getenv("ARGON_MEMORY_COST", 65536))
ARGON_PARALLELISM = int(os.getenv("ARGON_PARALLELISM", 4))
ARGON_HASH_LENGTH = int(os.getenv("ARGON_HASH_LENGTH", 32))
ARGON_SALT_LENGTH = int(os.getenv("ARGON_SALT_LENGTH", 16))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "please1change1me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

argon2_hasher = PasswordHasher(
    time_cost=ARGON_TIME_COST,
    memory_cost=ARGON_MEMORY_COST,
    parallelism=ARGON_PARALLELISM,
    hash_len=ARGON_HASH_LENGTH,
    salt_len=ARGON_SALT_LENGTH,
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

Oauth2_bearer_dep = Annotated[str, Depends(oauth2_bearer)]


async def get_current_user(token: Oauth2_bearer_dep):
    """Retrieve the current user based on the provided OAuth2 token.

    Parameters
    ----------
    token : oauth2_bearer_dep
        The OAuth2 bearer token used for authentication.

    Returns:
    -------
    dict
        A dictionary containing the name, role and user ID.

    Raises:
    ------
    HTTPException
        If the token is invalid or the user cannot be validated.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        name: str = payload.get("name")
        role: UserRole = payload.get("role")
        user_id: str = payload.get("id")
        faculty: Faculty = payload.get("faculty")
        if name is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"name": name, "id": user_id, "role": role, "faculty": faculty}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )


User_dep = Annotated[dict, Depends(get_current_user)]


def get_db():
    """Get a database session.

    This function provides a database session for interacting with the
    database. It ensures that the session is properly closed after use.

    Yields:
    -------
    Session
        A SQLAlchemy database session.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]
