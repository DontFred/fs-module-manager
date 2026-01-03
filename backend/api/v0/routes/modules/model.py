"""This module defines Pydantic models for module-related responses.

It includes models for listing modules, detailed module information,
and translations, along with their attributes and configurations.
"""

import enum
import uuid
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from api.model import SortOrder
from api.v0.routes.users.model import UserResponse
from db.model import Faculty
from db.model import WorkflowStatus


class TranslationResponse(BaseModel):
    """A response model representing a translation in the system.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the translation.
    language : str
        The language of the translation.
    title : str
        The title of the translation.
    content : str
        The content of the translation.
    is_outdated : bool
        Indicates if the translation is outdated.
    """

    id: uuid.UUID = Field(
        ..., description="The unique identifier for the translation"
    )
    language: str = Field(..., description="The language of the translation")
    title: str = Field(..., description="The title of the translation")
    content: str = Field(..., description="The content of the translation")
    is_outdated: bool = Field(
        ..., description="Indicates if the translation is outdated"
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleVersionResponse(BaseModel):
    """A response model representing a specific version of a module.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the module version.
    valid_from_semester : str
        The semester from which this version is valid.
    status : WorkflowStatus
        The workflow status of the module version.
    ects : int | None
        The ECTS credits associated with the module version.
    content : str | None
        The content description of the module version.
    updated_at : datetime
        The timestamp of the last update to the module version.
    last_editor : UserResponse
        The user who last edited the module version.
    translations : list[TranslationResponse]
        A list of translations associated with the module version.
    """

    id: uuid.UUID = Field(
        ..., description="The unique identifier for the module version"
    )
    valid_from_semester: str = Field(
        ..., description="The semester from which this version is valid"
    )
    status: WorkflowStatus = Field(
        ..., description="The workflow status of the module version"
    )
    ects: int | None = Field(
        None, description="The ECTS credits associated with the module version"
    )
    content: str | None = Field(
        None, description="The content description of the module version"
    )
    updated_at: datetime = Field(
        ...,
        description="The timestamp of the last update to the module version",
    )
    last_editor: UserResponse = Field(
        ..., description="The user who last edited the module version"
    )
    translations: list[TranslationResponse] = Field(
        ...,
        description="A list of translations associated with the module version",
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleVersionCompact(BaseModel):
    """A compact response model representing a version of a module.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the module version.
    valid_from_semester : str
        The semester from which this version is valid.
    status : WorkflowStatus
        The workflow status of the module version.
    updated_at : datetime
        The timestamp of the last update to the module version.
    last_editor_name : str
        The name of the user who last edited the module version.
    """

    id: uuid.UUID = Field(
        ..., description="The unique identifier for the module version"
    )
    valid_from_semester: str = Field(
        ..., description="The semester from which this version is valid"
    )
    status: WorkflowStatus = Field(
        ..., description="The workflow status of the module version"
    )
    updated_at: datetime = Field(
        ...,
        description="The timestamp of the last update to the module version",
    )
    last_editor_name: str = Field(
        ...,
        description="The name of the user who last edited the module version",
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleListResponse(BaseModel):
    """A response model representing a module in the system.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the module.
    module_number : str
        The module number.
    title : str
        The title of the module.
    owner : UserResponse
        The owner of the module.
    faculty : str
        The faculty of the module.
    current_semester : str
        The current semester of the module.
    current_status : WorkflowStatus
        The current status of the module.
    """

    id: uuid.UUID = Field(
        ..., description="The unique identifier for the module"
    )
    module_number: str = Field(..., description="The module number")
    title: str = Field(..., description="The title of the module")
    owner: UserResponse = Field(..., description="The owner of the module")
    faculty: Faculty = Field(..., description="The faculty of the module")
    current_semester: str = Field(
        ..., description="The current semester of the module"
    )
    current_status: WorkflowStatus = Field(
        ..., description="The current status of the module"
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleDetailResponse(BaseModel):
    """A response model representing detailed information about a module.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the module.
    module_number : str
        The module number.
    title : str
        The title of the module.
    faculty : str
        The faculty of the module.
    owner : UserResponse
        The owner of the module.
    current_version : ModuleVersionResponse
        The current version of the module with detailed information.
    history_summary : list[ModuleVersionCompact]
        A list of previous module versions for history summary.
    """

    id: uuid.UUID = Field(
        ..., description="The unique identifier for the module"
    )
    module_number: str = Field(..., description="The module number")
    title: str = Field(..., description="The title of the module")
    faculty: Faculty = Field(..., description="The faculty of the module")
    owner: UserResponse = Field(..., description="The owner of the module")
    current_version: ModuleVersionResponse = Field(
        ...,
        description="The current version of the module with details",
    )
    history_summary: list[ModuleVersionCompact] = Field(
        ...,
        description="A list of previous module versions for history summary",
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleFields(str, enum.Enum):
    """Enum for module fields.

    This enum defines the fields that can be selected when retrieving module
    data.
    """

    id = "id"
    module_number = "module_number"
    title = "title"
    faculty = "faculty"
    owner = "owner"
    current_semester = "current_semester"
    current_status = "current_status"


class AllModulesQueryParams:
    """Query parameters for retrieving all modules.

    This class defines the query parameters used for filtering, sorting,
    paginating, and selecting fields when retrieving a list of modules.

    Attributes:
    ----------
    faculty : Faculty | None
        Filter by faculty.
    owner_id : str | None
        Filter by owner user ID.
    current_semester : str | None
        Filter by current semester.
    current_status : WorkflowStatus | None
        Filter by current workflow status.
    search : str | None
        Search by title or module number.
    sort_by : ModuleFields
        Field to sort by.
    sort_order : SortOrder
        Sort order (ascending or descending).
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
        owner_id: str | None = Query(
            None, description="Filter by owner user ID"
        ),
        current_semester: str | None = Query(
            None, description="Filter by current semester"
        ),
        current_status: WorkflowStatus | None = Query(
            None, description="Filter by current workflow status"
        ),
        search: str | None = Query(
            None, description="Search by title or module number"
        ),
        # Sorting
        sort_by: ModuleFields = Query(
            "id",
            pattern="^("
            + "|".join([field.value for field in ModuleFields])
            + ")$",
            description=(
                "Field to sort by (id, module_number, title, faculty, owner, "
                + "current_semester, current_status)"
            ),
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
                "(e.g. 'id,title')",
            ),
        ),
    ):
        """Initialize query parameters for retrieving all modules.

        Args:
            faculty (Faculty | None): Filter by faculty.
            owner_id (str | None): Filter by owner user ID.
            current_semester (str | None): Filter by current semester.
            current_status (WorkflowStatus | None): Filter by current workflow
                status.
            search (str | None): Search by title or module number.
            sort_by (ModuleFields): Field to sort by.
            sort_order (SortOrder): Sort order (ascending or descending).
            page (int): Page number for pagination.
            limit (int): Number of items per page.
            offset (int): Number of items to skip.
            fields (str | None): Comma-separated list of fields to include in
                the response.
        """
        self.faculty = faculty
        self.owner_id = owner_id
        self.current_semester = current_semester
        self.current_status = current_status
        self.search = search
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.page = page
        self.limit = limit
        self.offset = offset
        self.fields = fields
