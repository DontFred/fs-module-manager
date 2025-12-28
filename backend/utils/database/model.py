"""This module contains utility classes and enums for database operations.

It includes:
- PaginationMeta: Metadata for paginated responses.
- PaginatedResponse: A generic model for paginated responses.
- SortOrder: Enum for specifying sort order.
- FieldSelectionParams: Class for handling field selection query parameters.
"""

import enum
from typing import TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Metadata for pagination.

    Attributes:
    ----------
    total : int
        Total number of items.
    page : int
        Current page number.
    limit : int
        Number of items per page.
    offset : int
        Number of items initially skipped.
    total_pages : int
        Total number of pages.
    """

    total: int
    page: int
    limit: int
    offset: int
    total_pages: int


class PaginatedResponse[T](BaseModel):
    """A generic paginated response model.

    Attributes:
    ----------
    data : list[T]
        The list of items in the current page.
    meta : PaginationMeta
        Metadata about the pagination, including total items, page number, and
        size.
    """

    data: list[T]
    meta: PaginationMeta


class SortOrder(str, enum.Enum):
    """Enum for sort order.

    This enum defines the possible sort orders for retrieving user data.
    """

    ASC = "asc"
    DESC = "desc"


class FieldSelectionParams:
    """Query parameters for retrieving a single obj.

    This class defines the query parameters that can be used to select
    specific fields when retrieving a single obj.

    Attributes:
    ----------
    fields : str | None
        Comma-separated list of fields to include in the response.
    """

    def __init__(
        self,
        # Field selection
        fields: str | None = Query(
            None,
            description=(
                "Comma-separated list of fields to include in the response",
                "(e.g. 'id,name')",
            ),
        ),
    ):
        """Initialize query parameters for retrieving a single user.

        Args:
            fields (str | None): Comma-separated list of fields to include in
                the response.
        """
        self.fields = fields
