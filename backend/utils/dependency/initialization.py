"""Module for dependency initialization in the backend.

This module provides utility functions and dependencies for:
- Retrieving the current user based on an OAuth2 token.
- Managing database sessions.
- Configuring security contexts and JWT handling.
"""

import os
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from dotenv import load_dotenv
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import SecurityScopes
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.initialization import engine

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

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="/v0/auth/token",
    scopes={
        "f1:module_owner": (
            "Access to module basic management features in faculty 1."
        ),
        "f2:module_owner": (
            "Access to module basic management features in faculty 2."
        ),
        "f3:module_owner": (
            "Access to module basic management features in faculty 3."
        ),
        "f4:module_owner": (
            "Access to module basic management features in faculty 4."
        ),
        "f1:program_coordinator": (
            "Access to program coordination features in faculty 1."
        ),
        "f2:program_coordinator": (
            "Access to program coordination features in faculty 2."
        ),
        "f3:program_coordinator": (
            "Access to program coordination features in faculty 3."
        ),
        "f4:program_coordinator": (
            "Access to program coordination features in faculty 4."
        ),
        "examination_office": "Access to examination office features.",
        "deanery": "Access to deanery features.",
        "admin": "Access to all administrative features.",
    },
)

oauth2_bearer_dep = Annotated[str, Depends(oauth2_bearer)]


class UserToken(BaseModel):
    """Represents a user token with authentication details.

    Attributes:
    ----------
    name : str
        The name of the user.
    id : str
        The unique identifier of the user.
    scopes : str
        The scopes or permissions assigned to the user.
    """

    name: str
    id: str
    scopes: str


async def get_current_user(
    security_scopes: SecurityScopes, token: oauth2_bearer_dep
):
    """Retrieve the current user based on the provided OAuth2 token.

    Parameters
    ----------
    token : oauth2_bearer_dep
        The OAuth2 bearer token used for authentication.

    Returns:
    -------
    UserToken
        The authenticated user's token information.

    Raises:
    ------
    HTTPException
        If the token is invalid or the user cannot be validated.
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        name: str = payload.get("name")
        user_id: str = payload.get("id")
        scopes: str = payload.get("scope")
        if name is None or user_id is None or scopes is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in scopes.split(" "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return UserToken(name=name, id=user_id, scopes=scopes)
    except Exception:
        raise credentials_exception


user_dep = Annotated[UserToken, Depends(get_current_user)]
user_f1module_owner_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f1:module_owner"])
]
user_f2module_owner_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f2:module_owner"])
]
user_f3module_owner_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f3:module_owner"])
]
user_f4module_owner_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f4:module_owner"])
]
user_f1program_coordinator_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f1:program_coordinator"])
]
user_f2program_coordinator_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f2:program_coordinator"])
]
user_f3program_coordinator_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f3:program_coordinator"])
]
user_f4program_coordinator_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["f4:program_coordinator"])
]
user_examination_office_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["examination_office"])
]
user_deanery_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["deanery"])
]
user_admin_dep = Annotated[
    UserToken, Security(get_current_user, scopes=["admin"])
]


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
