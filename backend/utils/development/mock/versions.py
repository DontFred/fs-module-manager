"""This module provides utilities for creating and managing mock version data.

It includes:
- VersionSchema: A Pydantic schema for version validation.
- mock_version: A function to generate mock Version objects for testing.
- get_mock_version:
    A function to retrieve mock versions as VersionSchema objects.
"""

from datetime import UTC
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from db.model import Module
from db.model import ModuleVersion
from db.model import WorkflowStatus


class VersionSchema(BaseModel):
    """A schema representing a module version.

    Attributes:
    ----------
    id : str
        The unique identifier for the module version.
    module_id : str
        The unique identifier for the associated module.
    content : str
        The content/details of the module version.
    valid_from_semester : str
        The semester from which the version is valid.
    ects : int
        The ECTS credits associated with the module version.
    status : WorkflowStatus
        The current workflow status of the module version.
    last_editor_id : str
        The unique identifier of the last editor of the module version.
    updated_at : str
        The timestamp of the last update to the module version.
    """

    id: str
    module_id: str
    content: str
    valid_from_semester: str
    ects: int
    status: WorkflowStatus
    last_editor_id: str
    updated_at: str
    model_config = ConfigDict(from_attributes=True)


def mock_versions(mock_version_data: list[Module]) -> list[ModuleVersion]:
    """Generate mock versions for a list of modules.

    Parameters:
    ----------
    mock_version_data : list[Module]
        A list of Module objects for which mock versions will be created.

    Returns:
    -------
    list[ModuleVersion]
        A list of ModuleVersion objects with mock data.
    """
    from utils.development.service import get_uuid_seeded

    versions: list[ModuleVersion] = []
    for module in mock_version_data:
        for idx in range(6):
            match idx % 6:
                case 0:
                    status = WorkflowStatus.RELEASED
                    semester = f"WiSe 202{3 + idx}/2{4 + idx}"
                case 1:
                    status = WorkflowStatus.APPROVAL_DEANERY
                    semester = f"SoSe 202{3 + idx}"
                case 2:
                    status = WorkflowStatus.VALIDATION_EO
                    semester = f"WiSe 202{3 + idx}/2{4 + idx}"
                case 3:
                    status = WorkflowStatus.IN_REVIEW
                    semester = f"SoSe 202{3 + idx}"
                case 4:
                    status = WorkflowStatus.DRAFT
                    semester = f"WiSe 202{3 + idx}/2{4 + idx}"
                case 5:
                    status = WorkflowStatus.IN_REVISION
                    semester = f"SoSe 202{3 + idx}"
            version = ModuleVersion(
                id=get_uuid_seeded(f"{module.module_number}-v{idx}"),
                module=module,
                content=f"Details für {module.title}. Version {idx + 1}",
                valid_from_semester=semester,
                ects=6,
                status=status,
                last_editor=module.owner,
                updated_at=datetime.now(UTC),
            )
            versions.append(version)
    return versions


def get_mock_versions() -> list[ModuleVersion]:
    """Retrieve mock ModuleVersion objects for development purposes.

    Returns:
    -------
    list[ModuleVersion]
        A list of ModuleVersion objects containing mock data.
    """
    from .modules import mock_modules
    from .user import mock_user

    users = mock_user()
    modules = mock_modules(users)
    for module in modules:
        module.owner_id = module.owner.user_id
    versions = mock_versions(modules)
    for version in versions:
        version.module_id = version.module.id
        version.last_editor_id = version.last_editor.user_id
        version.updated_at = version.updated_at.__str__()

    return [VersionSchema.model_validate(version) for version in versions]
