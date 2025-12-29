"""This module defines the models used for authentication.

It includes classes and functions related to user authentication and
authorization.
"""

from pydantic import BaseModel


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
    """Represents data stored in a token.

    Attributes:
    ----------
    id : str | None
        The unique identifier of the user (optional).
    name : str | None
        The name of the user (optional).
    scopes : list[str]
        The list of scopes or permissions associated with the token.
    """

    id: str | None = None
    name: str | None = None
    scopes: list[str] = []
