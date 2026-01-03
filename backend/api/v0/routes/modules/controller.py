"""Controller module for handling module-related API endpoints.

This module defines the API routes for managing modules, versions, and
translations. It connects the HTTP layer with the business logic service.
"""

import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from api.model import PaginatedResponse
from utils.dependency.initialization import db_dep
from utils.dependency.initialization import user_dep

from . import model
from . import service

router = APIRouter(prefix="/v0/modules", tags=["Modules"])


@router.get(
    "/",
    response_model=PaginatedResponse[model.ModuleResponse],
    response_model_exclude_unset=True,
)
def get_all_modules(
    db: db_dep,
    user_token: user_dep,
    response: Response,
    params: model.ModuleQueryParams = Depends(),
):
    """Retrieve all modules with optional filtering."""
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    return service.get_all_modules(db, user_token, response, params)


@router.post(
    "/",
    response_model=model.ModuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_module(
    module: model.ModuleCreate,
    db: db_dep,
    user_token: user_dep,
    response: Response,
):
    """Create a new module (and initial draft version)."""
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    if user_token.scopes not in {
        "f1:module_owner",
        "f2:module_owner",
        "f3:module_owner",
        "f4:module_owner",
        "admin",
    }:
        raise HTTPException(
            status_code=403,
            detail="Only Module Owners and Admins can create modules",
        )

    return service.create_module(module, db, user_token, response)


@router.get("/{module_id}", response_model=model.ModuleResponse)
def get_module(module_id: uuid.UUID, db: db_dep, user_token: user_dep):
    """Get a specific module by ID."""
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    return service.get_module_by_id(module_id, db, user_token)


@router.get(
    "/{module_id}/versions", response_model=list[model.ModuleVersionResponse]
)
def get_module_versions(
    module_id: uuid.UUID,
    db: db_dep,
    user_token: user_dep,
):
    """Get all versions of a specific module."""
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    return service.get_module_versions(module_id, db, user_token)


@router.get(
    "/versions/{version_id}", response_model=model.ModuleVersionResponse
)
def get_version(version_id: uuid.UUID, db: db_dep, user_token: user_dep):
    """Get details of a specific module version."""
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    return service.get_version_details(version_id, db, user_token)


@router.put(
    "/versions/{version_id}", response_model=model.ModuleVersionResponse
)
def update_version_content(
    version_id: uuid.UUID,
    update_data: model.ModuleVersionUpdate,
    db: db_dep,
    user_token: user_dep,
):
    """Update the content of a module version (Draft/Revision only).

    Args:
        version_id (uuid.UUID): The ID of the module version to update.
        update_data (model.ModuleVersionUpdate): The updated version data.
        db (db_dep): The database dependency for querying and persisting data.
        user_token (UserToken): Token containing information about the
            authenticated user.

    Returns:
        model.ModuleVersionResponse: The updated module version record.
    """
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    if user_token.scopes not in {
        "f1:module_owner",
        "f2:module_owner",
        "f3:module_owner",
        "f4:module_owner",
        "admin",
    }:
        raise HTTPException(
            status_code=403,
            detail="Only Module Owners and Admins can update module versions",
        )

    return service.update_version_content(
        version_id, update_data, db, user_token
    )


@router.patch(
    "/versions/{version_id}/status", response_model=model.ModuleVersionResponse
)
def update_workflow_status(
    version_id: uuid.UUID,
    status_update: model.ModuleVersionStatusUpdate,
    db: db_dep,
    user_token: user_dep,
):
    """Transition the workflow status of a version (e.g., Submit, Approve).

    Args:
        version_id (uuid.UUID): The ID of the module version to update.
        status_update (model.ModuleVersionStatusUpdate): The status update data.
        db (db_dep): The database dependency for querying and persisting data.
        user_token (UserToken): Token containing information about the
            authenticated user.

    Returns:
        model.ModuleVersionResponse: The updated module version record.
    """
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    return service.update_workflow_status(
        version_id, status_update, db, user_token
    )


@router.post(
    "/versions/{version_id}/translations",
    response_model=model.TranslationResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_translation(
    version_id: uuid.UUID,
    translation: model.TranslationCreate,
    db: db_dep,
    user_token: user_dep,
):
    """Add a translation to a module version.

    Args:
        version_id (uuid.UUID): The ID of the module version to add the
            translation to.
        translation (model.TranslationCreate): The translation data to add.
        db (db_dep): The database dependency for querying and persisting data.
        user_token (UserToken): Token containing information about the
            authenticated user.

    Returns:
        model.TranslationResponse: The created translation record.
    """
    if not user_token:
        raise HTTPException(status_code=401, detail="Authentication required")

    if user_token.scopes not in {
        "f1:module_owner",
        "f2:module_owner",
        "f3:module_owner",
        "f4:module_owner",
        "admin",
    }:
        raise HTTPException(
            status_code=403,
            detail="Only Module Owners and Admins can add translations",
        )

    return service.add_translation(version_id, translation, db, user_token)
