"""This module defines the models used for authentication.

It includes classes and functions related to user authentication and
authorization.
"""

from pydantic import BaseModel

from db.model import Faculty
from db.model import UserRole


class Token(BaseModel):
    """Represents an authentication token.

    Attributes:
    ----------
    access_token : str
        The access token string.
    token_type : str
        The type of the token, e.g., "Bearer".
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Represents data associated with an authentication token.

    Attributes:
    ----------
    name : str | None
        The name of the user associated with the token.
    faculty : Faculty | None
        The faculty or department of the user.
    role : UserRole | None
        The role of the user, e.g., "admin" or "student".
    """

    name: str | None = None
    faculty: Faculty | None = None
    role: UserRole | None = None
