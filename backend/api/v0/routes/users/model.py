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
    """Base model for user information.

    Attributes:
    ----------
    name : str
        The name of the user.
    faculty : Faculty
        The faculty of the user.
    role : UserRole
        The role of the user.
    """

    name: str = Field(..., description="The username of the user")
    faculty: Faculty = Field(..., description="The faculty of the user")
    role: UserRole = Field(..., description="The role of the user")


class UserCreate(UserBase):
    """Model for creating a new user.

    Attributes:
    ----------
    user_id : str
        The unique identifier for the user.
    username : str
        The username of the user.
    faculty : Faculty
        The faculty of the user.
    role : UserRole
        The role of the user.
    password : str
        The password of the user.
    """

    user_id: str = Field(..., description="The unique identifier for the user")
    password: str = Field(..., description="The password for the user")


class UserUpdate(UserBase):
    """Model for updating user information.

    Attributes:
    ----------
    name : str
        The name of the user.
    faculty : Faculty
        The faculty of the user.
    role : UserRole
        The role of the user.
    password : str
        The password of the user.
    """

    password: str = Field(..., description="The password for the user")


class UserPatch(UserBase):
    """Model for patching user information.

    Attributes:
    ----------
    name : str | None
        The name of the user.
    faculty : Faculty | None
        The faculty of the user.
    role : UserRole | None
        The role of the user.
    password : str | None
        The password of the user.
    """

    name: str | None = Field(None, description="The username of the user")
    faculty: Faculty | None = Field(None, description="The faculty of the user")
    role: UserRole | None = Field(None, description="The role of the user")
    password: str | None = Field(None, description="The password for the user")


class UserResponse(BaseModel):
    """Model for the user response.

    Attributes:
    ----------
    user_id : int | None
        The unique identifier for the user.
    name : str | None
        The name of the user.
    faculty : Faculty | None
        The faculty of the user.
    role : UserRole | None
        The role of the user.
    """

    user_id: str | None = Field(
        None, description="The unique identifier for the user"
    )
    name: str | None = Field(None, description="The username of the user")
    faculty: Faculty | None = Field(None, description="The faculty of the user")
    role: UserRole | None = Field(None, description="The role of the user")
    model_config = ConfigDict(from_attributes=True)


class UserFields(str, enum.Enum):
    """Enum for user fields.

    This enum defines the fields that can be selected when retrieving user
    data.
    """

    USER_ID = "user_id"
    NAME = "name"
    FACULTY = "faculty"
    ROLE = "role"


class AllUsersQueryParams:
    """Query parameters for retrieving all users.

    This class defines the query parameters that can be used to filter, sort,
    paginate, and select fields when retrieving a list of users.

    Attributes:
    ----------
    faculty : Faculty | None
        Filter by faculty.
    role : UserRole | None
        Filter by role.
    search : str | None
        Search by name.
    sort_by : UserFields
        Field to sort by (user_id, name, faculty, role).
    sort_order : SortOrder
        Sort order (asc or desc).
    page : int
        Page number for pagination.
    limit : int
        Number of items per page.
    offset : int
        Number of items to skip.
    fields : str | None
        Comma-separated list of fields to include in the response.
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
