"""This module provides utilities for creating and managing mock auditlogs data.

It includes:
- AuditlogsSchema: A Pydantic schema for auditlogs validation.
- mock_auditlogs: A function to generate mock auditlogs objects for testing.
- get_mock_auditlogs:
    A function to retrieve mock auditlogss as AuditlogsSchema objects.
"""

from datetime import timedelta

from pydantic import BaseModel
from pydantic import ConfigDict

from db.model import AuditLog
from db.model import ModuleVersion
from db.model import User
from db.model import WorkflowStatus


class AuditLogSchema(BaseModel):
    """A schema representing an audit log entry.

    Attributes:
    ----------
    id : str
        The unique identifier for the audit log entry.
    module_version_id : str
        The associated module version id for the audit log.
    user_id : str
        The user id who performed the action.
    action : str
        The action performed.
    comment : str | None
        An optional comment regarding the action.
    timestamp : str
        The timestamp when the action was performed.
    """

    id: str
    module_version_id: str
    user_id: str
    action: str
    comment: str | None
    timestamp: str
    model_config = ConfigDict(from_attributes=True)


def mock_auditlogs(
    mock_version_data: list[ModuleVersion], mock_user_data: list[User]
) -> list[AuditLog]:
    """Generate mock audit logs based on module version data and user data.

    Parameters:
    ----------
    mock_version_data : list[ModuleVersion]
        List of module version data to generate audit logs for.
    mock_user_data : list[User]
        List of user data to associate with the audit logs.

    Returns:
    -------
    list[AuditLog]
        A list of generated audit logs.
    """
    from utils.development.service import get_uuid_seeded

    auditlogs: list[AuditLog] = []

    exam = next(
        user
        for user in mock_user_data
        if user.role.value == "EXAMINATION_OFFICE"
    )
    dean = next(user for user in mock_user_data if user.role.value == "DEANERY")

    for version in mock_version_data:
        owner = version.last_editor

        coord = next(
            user
            for user in mock_user_data
            if user.faculty == owner.faculty
            and user.role.value == "PROGRAM_COORDINATOR"
        )

        ts = version.updated_at - timedelta(days=10)

        auditlogs.append(
            AuditLog(
                id=get_uuid_seeded(f"{version.id}-created"),
                module_version_id=version.id,
                user_id=owner.user_id,
                action="CREATED_DRAFT",
                timestamp=ts,
            )
        )

        if version.status == WorkflowStatus.IN_REVIEW:
            auditlogs.append(
                AuditLog(
                    id=get_uuid_seeded(f"auditlog-{version.id}-submitted"),
                    module_version_id=version.id,
                    user_id=owner.user_id,
                    action="SUBMITTED",
                    timestamp=ts + timedelta(days=1),
                )
            )

        elif version.status == WorkflowStatus.IN_REVISION:
            auditlogs.append(
                AuditLog(
                    id=get_uuid_seeded(f"auditlog-{version.id}-submitted"),
                    module_version_id=version.id,
                    user_id=owner.user_id,
                    action="SUBMITTED",
                    timestamp=ts + timedelta(days=1),
                )
            )
            auditlogs.append(
                AuditLog(
                    id=get_uuid_seeded(f"auditlog-{version.id}-rejected"),
                    module_version_id=version.id,
                    user_id=coord.user_id,
                    action="REJECTED",
                    comment="Lernziele unklar.",
                    timestamp=ts + timedelta(days=2),
                )
            )

        elif version.status == WorkflowStatus.VALIDATION_EO:
            auditlogs.append(
                AuditLog(
                    id=get_uuid_seeded(
                        f"auditlog-{version.id}-approved_content"
                    ),
                    module_version_id=version.id,
                    user_id=coord.user_id,
                    action="APPROVED_CONTENT",
                    comment="Sieht gut aus.",
                    timestamp=ts + timedelta(days=3),
                )
            )

        elif version.status == WorkflowStatus.APPROVAL_DEANERY:
            auditlogs.append(
                AuditLog(
                    id=get_uuid_seeded(f"auditlog-{version.id}-validated_ects"),
                    module_version_id=version.id,
                    user_id=exam.user_id,
                    action="VALIDATED_ECTS",
                    timestamp=ts + timedelta(days=4),
                )
            )

        elif version.status == WorkflowStatus.RELEASED:
            auditlogs.append(
                AuditLog(
                    id=get_uuid_seeded(f"auditlog-{version.id}-final_release"),
                    module_version_id=version.id,
                    user_id=dean.user_id,
                    action="FINAL_RELEASE",
                    timestamp=ts + timedelta(days=5),
                )
            )

    return auditlogs


def get_mock_auditlogs() -> list[AuditLogSchema]:
    """Retrieve mock AuditLogSchema objects for development purposes.

    Returns:
    -------
    list[AuditLogSchema]
        A list of AuditLogSchema objects containing mock data.
    """
    from .modules import mock_modules
    from .user import mock_user
    from .versions import mock_versions

    users = mock_user()
    modules = mock_modules(users)
    versions = mock_versions(modules)
    auditlogs = mock_auditlogs(versions, users)

    return [AuditLogSchema.model_validate(auditlog) for auditlog in auditlogs]
