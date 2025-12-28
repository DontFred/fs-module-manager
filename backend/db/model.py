"""This module defines the database models for the application.

It includes models for users, modules, module versions, translations, and audit
logs, as well as enumerations for user roles and workflow statuses.
"""

import enum
import uuid
from datetime import datetime
from datetime import timezone

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class UserRole(str, enum.Enum):
    """Enumeration of user roles within the application.

    Attributes:
    ----------
    MODULE_OWNER : str
        Represents a module owner.
    PROGRAM_COORDINATOR : str
        Represents a program coordinator.
    EXAMINATION_OFFICE : str
        Represents the examination office.
    DEANERY : str
        Represents the deanery.
    ADMIN : str
        Represents an server administrator.
    """

    MODULE_OWNER = "MODULE_OWNER"
    PROGRAM_COORDINATOR = "PROGRAM_COORDINATOR"
    EXAMINATION_OFFICE = "EXAMINATION_OFFICE"
    DEANERY = "DEANERY"
    ADMIN = "ADMIN"


class Faculty(str, enum.Enum):
    """Enumeration of faculties within the application.

    Attributes:
    ----------
    F1_MPM : str
        Represents FB1 the Faculty of Mechanical Engineering, Process
        Engineering, and Maritime Technology.
    F2_ELS : str
        Represents FB2 the Faculty of Energy and Life Sciences.
    F3_IC : str
        Represents FB3 the Faculty of Information and Communication.
    F4_BS : str
        Represents the Business School.
    ADMIN : str
        Represents administrative roles.
    """

    F1_MPM = "F1_MECHANICAL_PROCESS_MARITIME"
    F2_ELS = "F2_ENERGY_LIFE_SCIENCE"
    F3_IC = "F3_INFORMATION_COMMUNICATION"
    F4_BS = "F4_BUSINESS_SCHOOL"
    ADMIN = "ADMIN"


class WorkflowStatus(str, enum.Enum):
    """Enumeration of workflow statuses within the application.

    Attributes:
    ----------
    DRAFT : str
        Represents a draft status.
    IN_REVIEW : str
        Represents a status where the module is under review by the coordinator.
    VALIDATION_PA : str
        Represents a status where the module is being validated by the
        examination office.
    APPROVAL_DEANERY : str
        Represents a status where the module is awaiting approval from the
        deanery.
    RELEASED : str
        Represents a status where the module has been released.
    IN_REVISION : str
        Represents a status where the module is under revision.
    """

    DRAFT = "DRAFT"  # Entwurf
    IN_REVIEW = "IN_REVIEW"  # In Prüfung (Coordinator)
    VALIDATION_PA = "VALIDATION_PA"  # In Validierung (Prüfungsamt)
    APPROVAL_DEANERY = "APPROVAL_DEANERY"  # In Freigabe (Dekanat)
    RELEASED = "RELEASED"  # Freigegeben
    IN_REVISION = "IN_REVISION"


class User(Base):
    """Represents a user in the application.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the user.
    name : str
        The name of the user.
    role : UserRole
        The role of the user within the application.
    owned_modules : list[Module]
        The list of modules owned by the user.
    edited_versions : list[ModuleVersion]
        The list of module versions last edited by the user.
    """

    __tablename__ = "users"
    user_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    faculty: Mapped[Faculty] = mapped_column(Enum(Faculty), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    owned_modules: Mapped[list[Module]] = relationship(
        "Module", back_populates="owner"
    )
    edited_versions: Mapped[list[ModuleVersion]] = relationship(
        "ModuleVersion", back_populates="last_editor"
    )

    def __repr__(self):
        """Return a string representation of the user."""
        return (
            f"<User(id='{self.user_id}', name='{self.name}', "
            f"faculty='{self.faculty.value}', role='{self.role.value}')>"
        )


class Module(Base):
    """Represents a module in the application.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the module.
    module_number : str
        The unique module number (e.g., from HISinOne).
    title : str
        The title of the module.
    owner_id : Optional[str]
        The ID of the user who owns the module.
    owner : User
        The user who owns the module.
    versions : list[ModuleVersion]
        The list of versions associated with the module.
    """

    __tablename__ = "modules"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    module_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("users.user_id"))
    owner: Mapped[User] = relationship("User", back_populates="owned_modules")
    versions: Mapped[list[ModuleVersion]] = relationship(
        "ModuleVersion", back_populates="module", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """Return a string representation of the module."""
        return f"<Module(number='{self.module_number}', title='{self.title}')>"


class ModuleVersion(Base):
    """Represents a version of a module in the application.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the module version.
    module_id : uuid.UUID
        The ID of the module this version belongs to.
    content : Optional[str]
        The description of the module version.
    ects : Optional[int]
        The ECTS credits associated with the module version.
    valid_from_semester : str
        The semester from which this version is valid (e.g., "WiSe 2025").
    status : WorkflowStatus
        The workflow status of the module version.
    updated_at : datetime
        The timestamp of the last update to the module version.
    last_editor_id : Optional[str]
        The ID of the user who last edited the module version.
    module : Module
        The module this version belongs to.
    last_editor : User
        The user who last edited the module version.
    translations : list[Translation]
        The translations associated with the module version.
    audit_logs : list[AuditLog]
        The audit logs associated with the module version.
    """

    __tablename__ = "module_versions"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    module_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("modules.id"), nullable=False
    )
    content: Mapped[str | None] = mapped_column(Text)
    ects: Mapped[int | None] = mapped_column(Integer)
    valid_from_semester: Mapped[str] = mapped_column(String(20))
    status: Mapped[WorkflowStatus] = mapped_column(
        Enum(WorkflowStatus), default=WorkflowStatus.DRAFT
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.UTC),
        onupdate=lambda: datetime.now(timezone.UTC),
    )
    last_editor_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.user_id")
    )
    module: Mapped[Module] = relationship("Module", back_populates="versions")
    last_editor: Mapped[User] = relationship(
        "User", back_populates="edited_versions"
    )
    translations: Mapped[list[Translation]] = relationship(
        "Translation",
        back_populates="module_version",
        cascade="all, delete-orphan",
    )
    audit_logs: Mapped[list[AuditLog]] = relationship(
        "AuditLog", back_populates="module_version"
    )

    def __repr__(self):
        """Return a string representation of the module version."""
        return (
            f"<ModuleVersion(status='{self.status.value}', "
            f"semester='{self.valid_from_semester}')>"
        )


class Translation(Base):
    """Represents a translation of a module version in the application.

    Attributes:
    ----------
    id : uuid.UUID
        The unique identifier for the translation.
    module_version_id : uuid.UUID
        The ID of the module version this translation belongs to.
    language : str
        The language code of the translation (e.g., "EN").
    title : str
        The title of the translation.
    content : str
        The content of the translation.
    is_outdated : bool
        Indicates whether the translation is outdated.
    module_version : ModuleVersion
        The module version this translation belongs to.
    """

    __tablename__ = "translations"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    module_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("module_versions.id"), nullable=False
    )
    language: Mapped[str] = mapped_column(String(2), default="EN")
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    is_outdated: Mapped[bool] = mapped_column(Boolean, default=False)
    module_version: Mapped[ModuleVersion] = relationship(
        "ModuleVersion", back_populates="translations"
    )

    def __repr__(self):
        """Return a string representation of the translation."""
        return (
            f"<Translation(lang='{self.language}', title='{self.title}', "
            f"outdated={self.is_outdated})>"
        )


class AuditLog(Base):
    """Represents an audit log entry in the application.

    Attributes:
    ----------
    id : int
        The unique identifier for the audit log entry.
    module_version_id : uuid.UUID
        The ID of the module version this log entry is associated with.
    id : str
        The ID of the user who performed the action.
    action : str
        The action performed (e.g., "CREATE", "UPDATE").
    comment : Optional[str]
        Additional comments or details about the action.
    timestamp : datetime
        The timestamp when the action was performed.
    module_version : ModuleVersion
        The module version this log entry is associated with.
    user : User
        The user who performed the action.
    """

    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    module_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("module_versions.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str | None] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC)
    )
    module_version: Mapped[ModuleVersion] = relationship(
        "ModuleVersion", back_populates="audit_logs"
    )
    user: Mapped[User] = relationship("User")

    def __repr__(self):
        """Return a string representation of the audit log."""
        return (
            f"<AuditLog(action='{self.action}', user='{self.id}', "
            f"time='{self.timestamp}')>"
        )
