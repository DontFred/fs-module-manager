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
