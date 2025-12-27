"""This module defines Pydantic models for user-related data.

It includes base models for user information, models for creating new users,
and models for user responses.
"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from db.model import UserRole


class UserBase(BaseModel):
    """Base model for user information.

    Attributes:
    ----------
    name : str
        The name of the user.
    role : UserRole
        The role of the user.
    """

    name: str = Field(..., description="The username of the user")
    role: UserRole = Field(..., description="The role of the user")


class UserUpdate(UserBase):
    """Model for updating user information.

    Attributes:
    ----------
    name : str
        The name of the user.
    role : UserRole
        The role of the user.
    password : str
        The password of the user.
    """

    password: str = Field(..., description="The password for the user")


class UserCreate(UserBase):
    """Model for creating a new user.

    Attributes:
    ----------
    user_id : str
        The unique identifier for the user.
    username : str
        The username of the user.
    role : UserRole
        The role of the user.
    """

    user_id: str = Field(..., description="The unique identifier for the user")
    password: str = Field(..., description="The password for the user")


class UserResponse(UserBase):
    """Model for the user response.

    Attributes:
    ----------
    user_id : str
        The unique identifier for the user.
    name : str
        The name of the user.
    role : UserRole
        The role of the user.
    """

    user_id: str = Field(..., description="The unique identifier for the user")
    model_config = ConfigDict(from_attributes=True)
