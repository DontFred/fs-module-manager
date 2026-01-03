"""This module defines Pydantic models for module-related data.

It includes models for creating and retrieving modules, versions, translations,
and audit logs, as well as query parameters for filtering.
"""

import enum
import uuid
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from api.model import SortOrder
from db.model import Faculty
from db.model import WorkflowStatus


class AuditLogResponse(BaseModel):
    """Response model for audit log entries.

    Attributes:
        id (uuid.UUID): Unique identifier for the audit log.
        action (str): Action performed.
        comment (str | None): Optional comment.
        timestamp (datetime): Timestamp of the action.
        user_id (str): ID of the user who performed the action.
        user_name (str | None): Name of the user who performed the action.
    """

    id: uuid.UUID = Field(
        ..., description="Unique identifier for the audit log"
    )
    action: str = Field(..., description="Action performed")
    comment: str | None = Field(None, description="Optional comment")
    timestamp: datetime = Field(..., description="Timestamp of the action")
    user_id: str = Field(
        ..., description="ID of the user who performed the action"
    )
    user_name: str | None = Field(
        None, description="Name of the user who performed the action"
    )
    model_config = ConfigDict(from_attributes=True)


class TranslationBase(BaseModel):
    """Base model for translation data.

    Attributes:
        language (str): Language code (e.g., 'en').
        title (str): Translated title.
        content (str): Translated content.
    """

    language: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Language code (e.g., 'en')",
    )
    title: str = Field(..., description="Translated title")
    content: str = Field(..., description="Translated content")
    model_config = ConfigDict(from_attributes=True)


class TranslationCreate(TranslationBase):
    """Model for creating a translation.

    Attributes:
        language (str): Language code (e.g., 'en').
        title (str): Translated title.
        content (str): Translated content.
    """

    pass


class TranslationUpdate(BaseModel):
    """Model for updating a translation.

    Attributes:
        title (str | None): Updated translated title.
        content (str | None): Updated translated content.
        is_outdated (bool | None): Indicates if the translation is outdated.
    """

    title: str | None = Field(None, description="Translated title")
    content: str | None = Field(None, description="Translated content")
    is_outdated: bool | None = Field(
        None, description="Indicates if the translation is outdated"
    )
    model_config = ConfigDict(from_attributes=True)


class TranslationResponse(TranslationBase):
    """Response model for translations.

    Attributes:
        id (uuid.UUID): Unique identifier for the translation.
        module_version_id (uuid.UUID): Associated module version ID.
        is_outdated (bool): Indicates if the translation is outdated.
        language (str): Language code (e.g., 'en').
        title (str): Translated title.
        content (str): Translated content.
    """

    id: uuid.UUID = Field(
        ..., description="Unique identifier for the translation"
    )
    module_version_id: uuid.UUID = Field(
        ..., description="Associated module version ID"
    )
    is_outdated: bool = Field(
        ..., description="Indicates if the translation is outdated"
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleVersionBase(BaseModel):
    """Base model for module version data.

    Attributes:
        content (str | None): Content of the module version.
        ects (int | None): ECTS credits for the module version.
        valid_from_semester (str): Semester from which the module version is
            valid.
    """

    content: str | None = Field(None, description="Module version content")
    ects: int | None = Field(None, ge=0, description="ECTS credits")
    valid_from_semester: str = Field(..., description="e.g. 'WiSe 2025/26'")
    model_config = ConfigDict(from_attributes=True)


class ModuleVersionCreate(ModuleVersionBase):
    """Model for creating a module version.

    Attributes:
        content (str | None): Content of the module version.
        ects (int | None): ECTS credits for the module version.
        valid_from_semester (str): Semester from which the module version is
            valid.
    """

    pass


class ModuleVersionUpdate(BaseModel):
    """Model for updating a module version.

    Attributes:
        content (str | None): Updated content of the module version.
        ects (int | None): Updated ECTS credits for the module version.
        valid_from_semester (str | None): Updated semester from which the module
            version is valid.
    """

    content: str | None = Field(None, description="Module version content")
    ects: int | None = Field(None, ge=0, description="ECTS credits")
    valid_from_semester: str | None = Field(
        None, description="e.g. 'WiSe 2025/26'"
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleVersionStatusUpdate(BaseModel):
    """Model for updating the status of a module version.

    Attributes:
        status (WorkflowStatus): New workflow status to be set.
        comment (str | None): Optional reason for rejection or approval note.
    """

    status: WorkflowStatus = Field(..., description="New workflow status")
    comment: str | None = Field(
        None, description="Reason for rejection or approval note"
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleVersionResponse(ModuleVersionBase):
    """Response model for module versions.

    Attributes:
        id (uuid.UUID): Unique identifier for the module version.
        module_id (uuid.UUID): Associated module ID.
        status (WorkflowStatus): Current workflow status of the module version.
        updated_at (datetime): Timestamp of the last update.
        last_editor_id (str | None): ID of the last editor.
        translations (list[TranslationResponse]): List of translations.
        audit_logs (list[AuditLogResponse]): List of audit log entries.
        content (str | None): Content of the module version.
        ects (int | None): ECTS credits for the module version.
        valid_from_semester (str): Semester from which the module version is
            valid.
    """

    id: uuid.UUID = Field(
        ..., description="Unique identifier for the module version"
    )
    module_id: uuid.UUID = Field(..., description="Associated module ID")
    status: WorkflowStatus = Field(
        ..., description="Current workflow status of the module version"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp of the last update"
    )
    last_editor_id: str | None = Field(
        None, description="ID of the last editor"
    )
    translations: list[TranslationResponse] = Field(
        default_factory=list, description="List of translations"
    )
    audit_logs: list[AuditLogResponse] = Field(
        default_factory=list, description="List of audit log entries"
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleBase(BaseModel):
    """Base model for module data.

    Attributes:
        module_number (str): Unique module number.
        title (str): Title of the module.
    """

    module_number: str = Field(..., description="Unique module number")
    title: str = Field(..., description="Module title")
    model_config = ConfigDict(from_attributes=True)


class ModuleCreate(ModuleBase):
    """Model for creating a module.

    Attributes:
        module_number (str): Unique module number.
        title (str): Title of the module.
        content (str | None): Initial description of the module.
        ects (int): ECTS credits for the module.
        valid_from_semester (str): Semester from which the module is valid.
    """

    owner_id: str | None = Field(None, description="Owner user ID")
    content: str | None = Field(None, description="Initial description")
    ects: int = Field(..., ge=1, description="ECTS credits")
    valid_from_semester: str = Field(..., description="Valid from semester")
    model_config = ConfigDict(from_attributes=True)


class ModuleUpdate(BaseModel):
    """Model for updating a module.

    Attributes:
        module_number (str | None): Updated unique module number.
        title (str | None): Updated title of the module.
        owner_id (str | None): Updated owner user ID.
    """

    module_number: str | None = Field(None, description="Unique module number")
    title: str | None = Field(None, description="Module title")
    owner_id: str | None = Field(None, description="Owner user ID")
    model_config = ConfigDict(from_attributes=True)


class ModuleResponse(ModuleBase):
    """Response model for modules.

    Attributes:
        id (uuid.UUID): Unique identifier for the module.
        owner_id (str | None): Owner user ID.
        current_version (ModuleVersionResponse | None): Current module version.
    """

    id: uuid.UUID = Field(..., description="Unique identifier for the module")
    owner_id: str | None = Field(None, description="Owner user ID")
    current_version: ModuleVersionResponse | None = Field(
        None, description="Current module version"
    )
    released_version: ModuleVersionResponse | None = Field(
        None, description="Latest released module version"
    )
    model_config = ConfigDict(from_attributes=True)


class ModuleFields(str, enum.Enum):
    """Enumeration of fields for sorting modules.

    Attributes:
        MODULE_NUMBER (str): Field for module number.
        TITLE (str): Field for module title.
        OWNER (str): Field for module owner.
        UPDATED_AT (str): Field for last updated timestamp.
    """

    MODULE_NUMBER = "module_number"
    TITLE = "title"
    OWNER = "owner"
    UPDATED_AT = "updated_at"


class ModuleQueryParams:
    """Query parameters for filtering and sorting modules.

    Attributes:
        faculty (Faculty | None): Filter by faculty.
        owner_id (str | None): Filter by owner ID.
        status (WorkflowStatus | None): Filter by current version status.
        search (str | None): Search in title or number.
        sort_by (ModuleFields): Field to sort by.
        sort_order (SortOrder): Sort order (ascending or descending).
        page (int): Page number for pagination.
        limit (int): Number of items per page.
        offset (int): Number of items to skip.
        fields (str | None): Comma-separated list of fields to include in the
            response.
    """

    def __init__(
        self,
        faculty: Faculty | None = Query(None, description="Filter by faculty"),
        owner_id: str | None = Query(None, description="Filter by owner ID"),
        status: WorkflowStatus | None = Query(
            None, description="Filter by current version status"
        ),
        search: str | None = Query(
            None, description="Search in title or number"
        ),
        sort_by: ModuleFields = Query(
            ModuleFields.TITLE, description="Field to sort by"
        ),
        sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(50, ge=1, le=100, description="Items per page"),
        offset: int = Query(0, ge=0, description="Number of items to skip"),
        # Field selection
        fields: str | None = Query(
            None,
            description=(
                "Comma-separated list of fields to include in the response",
                "(e.g. 'id,module_number,title')",
            ),
        ),
    ):
        """Initialize query parameters for filtering and sorting modules.

        Args:
            faculty (Faculty | None): Filter by faculty.
            owner_id (str | None): Filter by owner ID.
            status (WorkflowStatus | None): Filter by current version status.
            search (str | None): Search in title or number.
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
        self.status = status
        self.search = search
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.page = page
        self.limit = limit
        self.offset = offset
        self.fields = fields
