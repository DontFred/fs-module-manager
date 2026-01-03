"""This module provides services for managing modules and their lifecycle.

It includes functions to CRUD modules, manage versions, handle workflow
transitions, and manage translations, while ensuring data consistency and
audit logging.
"""

import uuid
from datetime import UTC
from datetime import datetime

from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from api.model import PaginatedResponse
from db.model import AuditLog
from db.model import Faculty
from db.model import Module
from db.model import ModuleVersion
from db.model import Translation
from db.model import User
from db.model import WorkflowStatus
from utils.dependency.initialization import UserToken
from utils.dependency.initialization import db_dep
from utils.logging.initialization import logger

from . import model


def _create_audit_log(
    db: db_dep,
    version_id: uuid.UUID,
    user_id: str,
    action: str,
    comment: str | None = None,
):
    log = AuditLog(
        module_version_id=version_id,
        user_id=user_id,
        action=action,
        comment=comment,
        timestamp=datetime.now(UTC),
    )
    db.add(log)


def get_all_modules(
    db: db_dep,
    user_token: UserToken,
    response: Response,
    params: model.ModuleQueryParams,
) -> PaginatedResponse[model.ModuleResponse]:
    """Retrieve all modules with optional filtering, sorting, and pagination.

    Parameters:
    ----------
    db : db_dep
        The database dependency for querying.
    user_token : UserToken
        Token containing information about the authenticated user.
    response : Response
        The FastAPI response object to set status codes.
    params : model.ModuleQueryParams
        Query parameters for filtering, sorting, and pagination.

    Returns:
    -------
    PaginatedResponse[model.ModuleResponse]
        A paginated response containing the list of modules.

    Raises:
    ------
    HTTPException
        If an error occurs during the retrieval process.
    """
    try:
        query = db.query(Module)

        if params.faculty:
            query = query.join(User, Module.owner_id == User.user_id).filter(
                User.faculty == params.faculty
            )

        if params.owner_id:
            query = query.filter(Module.owner_id == params.owner_id)

        if params.search:
            query = query.filter(
                or_(
                    Module.title.ilike(f"%{params.search}%"),
                    Module.module_number.ilike(f"%{params.search}%"),
                )
            )

        if params.status:
            query = query.join(ModuleVersion).filter(
                ModuleVersion.status == params.status
            )

        match params.sort_by:
            case model.ModuleFields.TITLE:
                sort_col = Module.title
            case model.ModuleFields.MODULE_NUMBER:
                sort_col = Module.module_number
            case model.ModuleFields.OWNER:
                sort_col = Module.owner_id
            case _:
                sort_col = Module.title

        if params.sort_order == "desc":
            query = query.order_by(desc(sort_col))
        else:
            query = query.order_by(asc(sort_col))

        total_items = query.count()
        query = query.offset(params.offset).limit(params.limit)

        modules = query.options(joinedload(Module.versions)).all()

        response.status_code = status.HTTP_200_OK

        response_data = []
        for mod in modules:
            match user_token.scopes:
                case "admin":
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.DRAFT,
                            WorkflowStatus.IN_REVIEW,
                            WorkflowStatus.VALIDATION_EO,
                            WorkflowStatus.APPROVAL_DEANERY,
                            WorkflowStatus.IN_REVISION,
                        ]
                    ]
                case "deanery":
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.APPROVAL_DEANERY,
                        ]
                    ]
                case "examination_office":
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.VALIDATION_EO,
                            WorkflowStatus.APPROVAL_DEANERY,
                        ]
                    ]
                case "f1:program_coordinator":
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.IN_REVIEW,
                            WorkflowStatus.VALIDATION_EO,
                            WorkflowStatus.APPROVAL_DEANERY,
                        ]
                        and mod.owner.faculty == Faculty.F1_MPM
                    ]
                case "f2:program_coordinator":
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.IN_REVIEW,
                            WorkflowStatus.VALIDATION_EO,
                            WorkflowStatus.APPROVAL_DEANERY,
                        ]
                        and mod.owner.faculty == Faculty.F2_ELS
                    ]
                case "f3:program_coordinator":
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.IN_REVIEW,
                            WorkflowStatus.VALIDATION_EO,
                            WorkflowStatus.APPROVAL_DEANERY,
                        ]
                        and mod.owner.faculty == Faculty.F3_IC
                    ]
                case "f4:program_coordinator":
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.IN_REVIEW,
                            WorkflowStatus.VALIDATION_EO,
                            WorkflowStatus.APPROVAL_DEANERY,
                        ]
                        and mod.owner.faculty == Faculty.F4_BS
                    ]
                case (
                    "f1:module_owner"
                    | "f2:module_owner"
                    | "f3:module_owner"
                    | "f4:module_owner"
                ):
                    stript_versions = [
                        vers
                        for vers in mod.versions
                        if vers.status
                        in [
                            WorkflowStatus.DRAFT,
                            WorkflowStatus.IN_REVIEW,
                            WorkflowStatus.VALIDATION_EO,
                            WorkflowStatus.APPROVAL_DEANERY,
                            WorkflowStatus.IN_REVISION,
                        ]
                        and mod.owner_id == user_token.id
                    ]
                case _:
                    stript_versions = []
            versions_allowed = [
                vers
                for vers in mod.versions
                if vers.status == WorkflowStatus.RELEASED
            ] + stript_versions
            latest_version = (
                sorted(
                    versions_allowed, key=lambda v: v.updated_at, reverse=True
                )[0]
                if mod.versions
                else None
            )
            latest_released_version = (
                sorted(
                    [
                        vers
                        for vers in mod.versions
                        if vers.status == WorkflowStatus.RELEASED
                    ],
                    key=lambda v: v.updated_at,
                    reverse=True,
                )[0]
                if mod.versions
                else None
            )

            mod_resp = model.ModuleResponse(
                id=mod.id,
                module_number=mod.module_number,
                title=mod.title,
                owner_id=mod.owner_id,
                current_version=model.ModuleVersionResponse.model_validate(
                    latest_version
                )
                if latest_version
                else None,
                released_version=model.ModuleVersionResponse.model_validate(
                    latest_released_version
                )
                if latest_released_version
                else None,
            )
            response_data.append(mod_resp)

        return PaginatedResponse[model.ModuleResponse](
            data=response_data,
            meta={
                "total": total_items,
                "page": params.page,
                "limit": params.limit,
                "offset": params.offset,
                "total_pages": int((total_items - params.offset) / params.limit)
                + 1
                if total_items > 0
                else 1,
            },
        )

    except Exception as e:
        logger.error(f"Error retrieving modules: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def create_module(
    module_data: model.ModuleCreate,
    db: db_dep,
    user_token: UserToken,
    response: Response,
) -> model.ModuleResponse:
    """Create a new module and its initial version.

    Parameters:
    ----------
    module_data : model.ModuleCreate
        Data required to create the module.
    db : db_dep
        The database dependency for querying and persisting data.
    user_token : UserToken
        Token containing information about the authenticated user.
    response : Response
        The FastAPI response object to set status codes.

    Returns:
    -------
    model.ModuleResponse
        The created module with its initial version.

    Raises:
    ------
    HTTPException
        If an error occurs during the creation process.
    """
    try:
        if user_token.scopes == "admin" and module_data.owner_id is not None:
            owner_id = module_data.owner_id
        else:
            owner_id = user_token.id

        new_module = Module(
            module_number=module_data.module_number,
            title=module_data.title,
            owner_id=owner_id,
        )
        db.add(new_module)
        db.flush()

        initial_version = ModuleVersion(
            module_id=new_module.id,
            content=module_data.content,
            ects=module_data.ects,
            valid_from_semester=module_data.valid_from_semester,
            status=WorkflowStatus.DRAFT,
            last_editor_id=user_token.id,
            updated_at=datetime.now(UTC),
        )
        db.add(initial_version)
        db.flush()

        _create_audit_log(
            db, initial_version.id, user_token.id, "CREATED_DRAFT"
        )

        db.commit()
        db.refresh(new_module)

        response.status_code = status.HTTP_201_CREATED

        return model.ModuleResponse(
            id=new_module.id,
            module_number=new_module.module_number,
            title=new_module.title,
            owner_id=new_module.owner_id,
            current_version=model.ModuleVersionResponse.model_validate(
                initial_version
            ),
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating module: {e}")
        raise HTTPException(status_code=500, detail="Could not create module.")


def get_module_by_id(
    module_id: uuid.UUID, db: db_dep, user_token: UserToken
) -> model.ModuleResponse:
    """Retrieve a module by its unique identifier.

    Parameters:
    ----------
    module_id : uuid.UUID
        The unique identifier of the module to retrieve.
    db : db_dep
        The database dependency for querying.
    user_token : UserToken
        Token containing information about the authenticated user.

    Returns:
    -------
    model.ModuleResponse
        The module details including its latest version.

    Raises:
    ------
    HTTPException
        If the module is not found.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    match user_token.scopes:
        case "admin":
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.DRAFT,
                    WorkflowStatus.IN_REVIEW,
                    WorkflowStatus.VALIDATION_EO,
                    WorkflowStatus.APPROVAL_DEANERY,
                    WorkflowStatus.IN_REVISION,
                ]
            ]
        case "deanery":
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.APPROVAL_DEANERY,
                ]
            ]
        case "examination_office":
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.VALIDATION_EO,
                    WorkflowStatus.APPROVAL_DEANERY,
                ]
            ]
        case "f1:program_coordinator":
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.IN_REVIEW,
                    WorkflowStatus.VALIDATION_EO,
                    WorkflowStatus.APPROVAL_DEANERY,
                ]
                and module.owner.faculty == Faculty.F1_MPM
            ]
        case "f2:program_coordinator":
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.IN_REVIEW,
                    WorkflowStatus.VALIDATION_EO,
                    WorkflowStatus.APPROVAL_DEANERY,
                ]
                and module.owner.faculty == Faculty.F2_ELS
            ]
        case "f3:program_coordinator":
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.IN_REVIEW,
                    WorkflowStatus.VALIDATION_EO,
                    WorkflowStatus.APPROVAL_DEANERY,
                ]
                and module.owner.faculty == Faculty.F3_IC
            ]
        case "f4:program_coordinator":
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.IN_REVIEW,
                    WorkflowStatus.VALIDATION_EO,
                    WorkflowStatus.APPROVAL_DEANERY,
                ]
                and module.owner.faculty == Faculty.F4_BS
            ]
        case (
            "f1:module_owner"
            | "f2:module_owner"
            | "f3:module_owner"
            | "f4:module_owner"
        ):
            stript_versions = [
                vers
                for vers in module.versions
                if vers.status
                in [
                    WorkflowStatus.DRAFT,
                    WorkflowStatus.IN_REVIEW,
                    WorkflowStatus.VALIDATION_EO,
                    WorkflowStatus.APPROVAL_DEANERY,
                    WorkflowStatus.IN_REVISION,
                ]
                and module.owner_id == user_token.id
            ]
        case _:
            stript_versions = []
    versions_allowed = [
        vers
        for vers in module.versions
        if vers.status == WorkflowStatus.RELEASED
    ] + stript_versions
    latest_version = (
        sorted(versions_allowed, key=lambda v: v.updated_at, reverse=True)[0]
        if module.versions
        else None
    )
    latest_released_version = (
        sorted(
            [
                vers
                for vers in module.versions
                if vers.status == WorkflowStatus.RELEASED
            ],
            key=lambda v: v.updated_at,
            reverse=True,
        )[0]
        if module.versions
        else None
    )

    return model.ModuleResponse(
        id=module.id,
        module_number=module.module_number,
        title=module.title,
        owner_id=module.owner_id,
        current_version=model.ModuleVersionResponse.model_validate(
            latest_version
        )
        if latest_version
        else None,
        released_version=model.ModuleVersionResponse.model_validate(
            latest_released_version
        )
        if latest_released_version
        else None,
    )


def get_module_versions(
    module_id: uuid.UUID, db: db_dep, user_token: UserToken
) -> list[model.ModuleVersionResponse]:
    """Retrieve all versions of a specific module.

    Parameters:
    ----------
    module_id : uuid.UUID
        The unique identifier of the module whose versions are to be retrieved.
    db : db_dep
        The database dependency for querying.

    Returns:
    -------
    list[model.ModuleVersionResponse]
        A list of module version details.

    Raises:
    ------
    HTTPException
        If the module is not found.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    query = db.query(ModuleVersion).filter(ModuleVersion.module_id == module_id)

    match user_token.scopes:
        case "admin":
            pass
        case "deanery":
            query = query.filter(
                or_(
                    ModuleVersion.status == WorkflowStatus.APPROVAL_DEANERY,
                    ModuleVersion.status == WorkflowStatus.RELEASED,
                )
            )
        case "examination_office":
            query = query.filter(
                or_(
                    ModuleVersion.status == WorkflowStatus.APPROVAL_DEANERY,
                    ModuleVersion.status == WorkflowStatus.VALIDATION_EO,
                    ModuleVersion.status == WorkflowStatus.RELEASED,
                )
            )
        case "f1:program_coordinator":
            query = (
                query.join(Module)
                .join(User)
                .filter(
                    or_(
                        ModuleVersion.status == WorkflowStatus.IN_REVIEW,
                        ModuleVersion.status == WorkflowStatus.VALIDATION_EO,
                        ModuleVersion.status == WorkflowStatus.APPROVAL_DEANERY,
                        ModuleVersion.status == WorkflowStatus.RELEASED,
                    ),
                    User.faculty == Faculty.F1_MPM,
                )
            )
        case "f2:program_coordinator":
            query = (
                query.join(Module)
                .join(User)
                .filter(
                    or_(
                        ModuleVersion.status == WorkflowStatus.IN_REVIEW,
                        ModuleVersion.status == WorkflowStatus.VALIDATION_EO,
                        ModuleVersion.status == WorkflowStatus.APPROVAL_DEANERY,
                        ModuleVersion.status == WorkflowStatus.RELEASED,
                    ),
                    User.faculty == Faculty.F2_ELS,
                )
            )
        case "f3:program_coordinator":
            query = (
                query.join(Module)
                .join(User)
                .filter(
                    or_(
                        ModuleVersion.status == WorkflowStatus.IN_REVIEW,
                        ModuleVersion.status == WorkflowStatus.VALIDATION_EO,
                        ModuleVersion.status == WorkflowStatus.APPROVAL_DEANERY,
                        ModuleVersion.status == WorkflowStatus.RELEASED,
                    ),
                    User.faculty == Faculty.F3_IC,
                )
            )
        case "f4:program_coordinator":
            query = (
                query.join(Module)
                .join(User)
                .filter(
                    or_(
                        ModuleVersion.status == WorkflowStatus.IN_REVIEW,
                        ModuleVersion.status == WorkflowStatus.VALIDATION_EO,
                        ModuleVersion.status == WorkflowStatus.APPROVAL_DEANERY,
                        ModuleVersion.status == WorkflowStatus.RELEASED,
                    ),
                    User.faculty == Faculty.F4_BS,
                )
            )
        case (
            "f1:module_owner"
            | "f2:module_owner"
            | "f3:module_owner"
            | "f4:module_owner"
        ):
            query = query.filter(
                or_(
                    ModuleVersion.module.has(owner_id=user_token.id),
                    ModuleVersion.status == WorkflowStatus.RELEASED,
                )
            )

    versions = query.order_by(desc(ModuleVersion.updated_at)).all()

    return [
        model.ModuleVersionResponse.model_validate(version)
        for version in versions
    ]


def get_version_details(
    version_id: uuid.UUID, db: db_dep, user_token: UserToken
) -> model.ModuleVersionResponse:
    """Retrieve details of a specific module version.

    Parameters:
    ----------
    version_id : uuid.UUID
        The unique identifier of the module version to retrieve.
    db : db_dep
        The database dependency for querying.
    user_token : UserToken
        Token containing information about the authenticated user.

    Returns:
    -------
    model.ModuleVersionResponse
        The details of the specified module version.

    Raises:
    ------
    HTTPException
        If the module version is not found.
    """
    version = (
        db.query(ModuleVersion)
        .options(
            joinedload(ModuleVersion.translations),
            joinedload(ModuleVersion.audit_logs),
        )
        .filter(ModuleVersion.id == version_id)
        .first()
    )

    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    match user_token.scopes:
        case "admin":
            pass
        case "deanery":
            if version.status not in [
                WorkflowStatus.APPROVAL_DEANERY,
                WorkflowStatus.RELEASED,
            ]:
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this module version",
                )
        case "examination_office":
            if version.status not in [
                WorkflowStatus.VALIDATION_EO,
                WorkflowStatus.APPROVAL_DEANERY,
                WorkflowStatus.RELEASED,
            ]:
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this module version",
                )
        case "f1:program_coordinator":
            if not (
                (
                    version.status
                    in [
                        WorkflowStatus.IN_REVIEW,
                        WorkflowStatus.VALIDATION_EO,
                        WorkflowStatus.APPROVAL_DEANERY,
                    ]
                    and version.module.owner.faculty == Faculty.F1_MPM
                )
                or version.status == WorkflowStatus.RELEASED
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this module version",
                )
        case "f2:program_coordinator":
            if not (
                (
                    version.status
                    in [
                        WorkflowStatus.IN_REVIEW,
                        WorkflowStatus.VALIDATION_EO,
                        WorkflowStatus.APPROVAL_DEANERY,
                    ]
                    and version.module.owner.faculty == Faculty.F2_ELS
                )
                or version.status == WorkflowStatus.RELEASED
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this module version",
                )
        case "f3:program_coordinator":
            if not (
                (
                    version.status
                    in [
                        WorkflowStatus.IN_REVIEW,
                        WorkflowStatus.VALIDATION_EO,
                        WorkflowStatus.APPROVAL_DEANERY,
                    ]
                    and version.module.owner.faculty == Faculty.F3_IC
                )
                or version.status == WorkflowStatus.RELEASED
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this module version",
                )
        case "f4:program_coordinator":
            if not (
                (
                    version.status
                    in [
                        WorkflowStatus.IN_REVIEW,
                        WorkflowStatus.VALIDATION_EO,
                        WorkflowStatus.APPROVAL_DEANERY,
                    ]
                    and version.module.owner.faculty == Faculty.F4_BS
                )
                or version.status == WorkflowStatus.RELEASED
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this module version",
                )
        case (
            "f1:module_owner"
            | "f2:module_owner"
            | "f3:module_owner"
            | "f4:module_owner"
        ):
            if not (
                (
                    version.status
                    in [
                        WorkflowStatus.DRAFT,
                        WorkflowStatus.IN_REVIEW,
                        WorkflowStatus.VALIDATION_EO,
                        WorkflowStatus.APPROVAL_DEANERY,
                        WorkflowStatus.IN_REVISION,
                    ]
                    and version.module.owner_id == user_token.id
                )
                or version.status == WorkflowStatus.RELEASED
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied to this module version",
                )

    return model.ModuleVersionResponse.model_validate(version)


def update_version_content(
    version_id: uuid.UUID,
    update_data: model.ModuleVersionUpdate,
    db: db_dep,
    user_token: UserToken,
) -> model.ModuleVersionResponse:
    """Update the content of a specific module version.

    Parameters
    ----------
    version_id : uuid.UUID
        The unique identifier of the module version to update.
    update_data : model.ModuleVersionUpdate
        The data to update in the module version.
    db : db_dep
        The database dependency for querying and persisting data.
    user_token : UserToken
        Token containing information about the authenticated user.

    Returns:
    -------
    model.ModuleVersionResponse
        The updated module version details.

    Raises:
    ------
    HTTPException
        If the module version is not found or cannot be edited in its current
        status.
    """
    version = (
        db.query(ModuleVersion).filter(ModuleVersion.id == version_id).first()
    )
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    if version.status not in [WorkflowStatus.DRAFT, WorkflowStatus.IN_REVISION]:
        raise HTTPException(
            status_code=400, detail="Cannot edit version in current status."
        )

    if (
        user_token.id != version.module.owner_id
        and version.last_editor_id is not None
    ) or user_token.scopes != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only the owner can update this version.",
        )

    if update_data.content is not None:
        version.content = update_data.content
        for trans in version.translations:
            trans.is_outdated = True
    if update_data.ects is not None:
        version.ects = update_data.ects
    if update_data.valid_from_semester is not None:
        version.valid_from_semester = update_data.valid_from_semester

    version.last_editor_id = user_token.id
    version.updated_at = datetime.now(UTC)

    if update_data.content:
        for trans in version.translations:
            trans.is_outdated = True

    try:
        db.commit()
        db.refresh(version)
        return model.ModuleVersionResponse.model_validate(version)
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating version: {e}")
        raise HTTPException(status_code=500, detail="Update failed")


def update_workflow_status(
    version_id: uuid.UUID,
    status_data: model.ModuleVersionStatusUpdate,
    db: db_dep,
    user_token: UserToken,
) -> model.ModuleVersionResponse:
    """Update the workflow status of a specific module version.

    Parameters
    ----------
    version_id : uuid.UUID
        The unique identifier of the module version to update.
    status_data : model.ModuleVersionStatusUpdate
        The new workflow status and optional comment.
    db : db_dep
        The database dependency for querying and persisting data.
    user_token : UserToken
        Token containing information about the authenticated user.

    Returns:
    -------
    model.ModuleVersionResponse
        The updated module version details.

    Raises:
    ------
    HTTPException
        If the module version is not found or the status transition is invalid.
    """
    version = (
        db.query(ModuleVersion).filter(ModuleVersion.id == version_id).first()
    )
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    current_status = version.status
    new_status = status_data.status
    module_owner_id = version.module.owner_id

    if user_token.scopes == "admin":
        _create_audit_log(
            db,
            version.id,
            user_token.id,
            "ADMIN_STATUS_CHANGE",
            status_data.comment,
        )

    elif new_status == WorkflowStatus.IN_REVIEW:
        if (
            current_status
            not in [WorkflowStatus.DRAFT, WorkflowStatus.IN_REVISION]
        ) and user_token.id != module_owner_id:
            raise HTTPException(
                status_code=400, detail="Invalid transition to IN_REVIEW"
            )
        _create_audit_log(
            db, version.id, user_token.id, "SUBMITTED", status_data.comment
        )

    elif current_status == WorkflowStatus.IN_REVIEW:
        if new_status == WorkflowStatus.VALIDATION_EO and (
            user_token.scopes
            == (
                version.module.owner.faculty.value[:2].lower()
                + ":program_coordinator"
            )
        ):
            _create_audit_log(
                db,
                version.id,
                user_token.id,
                "APPROVED_CONTENT",
                status_data.comment,
            )
        elif new_status == WorkflowStatus.IN_REVISION and (
            user_token.scopes
            == (
                version.module.owner.faculty.value[:2].lower()
                + ":program_coordinator"
            )
            or user_token.id == module_owner_id
        ):
            _create_audit_log(
                db,
                version.id,
                user_token.id,
                "REJECTED_CONTENT",
                status_data.comment,
            )
        else:
            raise HTTPException(
                status_code=400, detail="Invalid transition from IN_REVIEW"
            )

    elif current_status == WorkflowStatus.VALIDATION_EO:
        if new_status == WorkflowStatus.APPROVAL_DEANERY and (
            user_token.scopes == "examination_office"
        ):
            _create_audit_log(
                db,
                version.id,
                user_token.id,
                "VALIDATED_ECTS",
                status_data.comment,
            )
        elif new_status == WorkflowStatus.IN_REVISION and (
            user_token.scopes == "examination_office"
            or user_token.id == module_owner_id
        ):
            _create_audit_log(
                db,
                version.id,
                user_token.id,
                "REJECTED_FORMAL",
                status_data.comment,
            )
        else:
            raise HTTPException(
                status_code=400, detail="Invalid transition from VALIDATION_EO"
            )

    elif current_status == WorkflowStatus.APPROVAL_DEANERY:
        if new_status == WorkflowStatus.RELEASED and (
            user_token.scopes == "deanery"
        ):
            _create_audit_log(
                db,
                version.id,
                user_token.id,
                "FINAL_RELEASE",
                status_data.comment,
            )
        elif new_status == WorkflowStatus.IN_REVISION and (
            user_token.scopes == "deanery" or user_token.id == module_owner_id
        ):
            _create_audit_log(
                db,
                version.id,
                user_token.id,
                "REJECTED_DEANERY",
                status_data.comment,
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid transition from APPROVAL_DEANERY",
            )

    else:
        raise HTTPException(
            status_code=400, detail="Invalid status transition requested."
        )

    version.status = new_status
    version.updated_at = datetime.now(UTC)

    try:
        db.commit()
        db.refresh(version)
        return model.ModuleVersionResponse.model_validate(version)
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating status: {e}")
        raise HTTPException(status_code=500, detail="Status update failed")


def add_translation(
    version_id: uuid.UUID,
    trans_data: model.TranslationCreate,
    db: db_dep,
    user_token: UserToken,
) -> model.TranslationResponse:
    """Add a new translation for a specific module version.

    Parameters:
    ----------
    version_id : uuid.UUID
        The unique identifier of the module version to which the translation
        belongs.
    trans_data : model.TranslationCreate
        The data for the new translation, including language, title, and
        content.
    db : db_dep
        The database dependency for querying and persisting data.
    user_token : UserToken
        Token containing information about the authenticated user.

    Returns:
    -------
    model.TranslationResponse
        The created translation details.

    Raises:
    ------
    HTTPException
        If the module version is not found or an error occurs during the
        creation process.
    """
    version = (
        db.query(ModuleVersion).filter(ModuleVersion.id == version_id).first()
    )
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    if (
        version.module.owner_id != user_token.id
        and user_token.scopes != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the Module Owner or Admin can add translations.",
        )
    new_trans = Translation(
        module_version_id=version_id,
        language=trans_data.language,
        title=trans_data.title,
        content=trans_data.content,
        is_outdated=False,
    )

    try:
        db.add(new_trans)
        db.commit()
        db.refresh(new_trans)

        return model.TranslationResponse.model_validate(new_trans)

    except Exception as e:
        db.rollback()
        logger.error(f"Error adding translation: {e}")
        raise HTTPException(status_code=500, detail="Could not add translation")
