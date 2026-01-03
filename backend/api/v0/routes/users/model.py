"""This module defines Pydantic models for user-related data.

It includes base models for user information, models for creating new users,
and models for user responses.
"""

import enum

from fastapi import Query
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from api.model import SortOrder
from db.model import Faculty
from db.model import UserRole


class UserBase(BaseModel):
    """Base model for user data.

    This class defines the common attributes for user-related data.

    Attributes:
        name (str): The username of the user.
        faculty (Faculty): The faculty of the user.
        role (UserRole): The role of the user.
    """

    name: str = Field(..., description="The username of the user")
    faculty: Faculty = Field(..., description="The faculty of the user")
    role: UserRole = Field(..., description="The role of the user")


class UserCreate(UserBase):
    """Model for creating a new user.

    This class defines the structure of the user data required for creating
    a new user.

    Attributes:
        user_id (str): The unique identifier for the user.
        password (str): The password for the user.
    """

    user_id: str = Field(..., description="The unique identifier for the user")
    password: str = Field(..., description="The password for the user")


class UserUpdate(UserBase):
    """Model for updating user data.

    This class defines the structure of the user data required for updating
    user information.

    Attributes:
        name (str): The username of the user.
        faculty (Faculty): The faculty of the user.
        role (UserRole): The role of the user.
        password (str): The password for the user.
    """

    password: str = Field(..., description="The password for the user")


class UserPatch(UserBase):
    """Model for partially updating user data.

    This class defines the structure of the user data that can be updated
    partially, with all fields being optional.

    Attributes:
        name (str | None): The username of the user.
        faculty (Faculty | None): The faculty of the user.
        role (UserRole | None): The role of the user.
        password (str | None): The password for the user.
    """

    name: str | None = Field(None, description="The username of the user")
    faculty: Faculty | None = Field(None, description="The faculty of the user")
    role: UserRole | None = Field(None, description="The role of the user")
    password: str | None = Field(None, description="The password for the user")


class UserResponse(BaseModel):
    """Response model for user data.

    This class defines the structure of the user data returned in API responses.

    Attributes:
        user_id (str | None): The unique identifier for the user.
        name (str | None): The username of the user.
        faculty (Faculty | None): The faculty of the user.
        role (UserRole | None): The role of the user.
    """

    user_id: str | None = Field(
        None, description="The unique identifier for the user"
    )
    name: str | None = Field(None, description="The username of the user")
    faculty: Faculty | None = Field(None, description="The faculty of the user")
    role: UserRole | None = Field(None, description="The role of the user")
    model_config = ConfigDict(from_attributes=True)


class UserFields(str, enum.Enum):
    """Enumeration of user fields for sorting and filtering.

    This class defines the fields that can be used for sorting and filtering
    user data in queries.
    """

    USER_ID = "user_id"
    NAME = "name"
    FACULTY = "faculty"
    ROLE = "role"


class AllUsersQueryParams:
    """Query parameters for retrieving all users.

    This class defines the filtering, sorting, pagination, and field selection
    options available when querying the list of users.

    Attributes:
        faculty (Faculty | None): Filter by faculty.
        role (UserRole | None): Filter by role.
        search (str | None): Search by name.
        sort_by (UserFields): Field to sort by (default: user_id).
        sort_order (SortOrder): Sort order (asc or desc, default: asc).
        page (int): Page number (default: 1).
        limit (int): Items per page (default: 50).
        offset (int): Items to skip (default: 0).
        fields (Optional[str]): Comma-separated list of fields to include in
            the response.
    """

    def __init__(
        self,
        # Filtering
        faculty: Faculty | None = Query(None, description="Filter by faculty"),
        role: UserRole | None = Query(None, description="Filter by role"),
        search: str | None = Query(None, description="Search by name"),
        # Sorting
        sort_by: UserFields = Query(
            "user_id",
            pattern="^("
            + "|".join([field.value for field in UserFields])
            + ")$",
            description="Field to sort by (user_id, name, faculty, role)",
        ),
        sort_order: SortOrder = Query(
            "asc",
            pattern="^("
            + "|".join([order.value for order in SortOrder])
            + ")$",
            description="Sort order (asc or desc)",
        ),
        # Pagination
        page: int = Query(1, ge=1, description="Page number for pagination"),
        limit: int = Query(
            50, ge=1, le=100, description="Number of items per page"
        ),
        offset: int = Query(0, ge=0, description="Number of items to skip"),
        # Field selection
        fields: str | None = Query(
            None,
            description=(
                "Comma-separated list of fields to include in the response",
                "(e.g. 'user_id,name')",
            ),
        ),
    ):
        """Initialize query parameters for retrieving all users.

        Args:
            faculty (Faculty | None): Filter by faculty.
            role (UserRole | None): Filter by role.
            search (str | None): Search by name.
            sort_by (UserFields): Field to sort by (user_id, name, faculty,
                role).
            sort_order (SortOrder): Sort order (asc or desc).
            page (int): Page number for pagination.
            limit (int): Number of items per page.
            offset (int): Number of items to skip.
            fields (str | None): Comma-separated list of fields to include in
                the response.
        """
        self.faculty = faculty
        self.role = role
        self.search = search
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.page = page
        self.limit = limit
        self.offset = offset
        self.fields = fields
