"""This module defines the API endpoints for user-related operations.

It includes endpoints for:
- Retrieving all users
- Creating a new user
- Retrieving a user by ID
- Updating a user's information
- Deleting a user
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response

from api.model import FieldSelectionParams
from api.model import PaginatedResponse
from utils.dependency.initialization import db_dep

from . import model
from . import service

router = APIRouter(prefix="/v0/users", tags=["Users"])


@router.get(
    "/",
    response_model=PaginatedResponse[model.UserResponse],
    response_model_exclude_unset=True,
    status_code=200,
)
def get_all_users(
    db: db_dep,
    response: Response,
    params: model.AllUsersQueryParams = Depends(),
):
    """Endpoint to retrieve a list of all users.

    Args:
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.
        params (model.AllUsersQueryParams): Query parameters for filtering
            users.

    Returns:
        PaginatedResponse[model.UserResponse]: A list of user data and
            pagination metadata.
    """
    all_users = service.get_all_users(db, response)

    # Filter
    if params.faculty:
        all_users = [
            user for user in all_users if user.faculty == params.faculty
        ]
    if params.role:
        all_users = [user for user in all_users if user.role == params.role]
    if params.search:
        search_lower = params.search.lower()
        all_users = [
            user
            for user in all_users
            if search_lower in user.name.lower()
            or search_lower in user.user_id.lower()
        ]
    # Sort
    if params.sort_by:
        reverse = params.sort_order == model.SortOrder.DESC.value
        all_users = sorted(
            all_users,
            key=lambda user: getattr(user, params.sort_by),
            reverse=reverse,
        )
    # Field Selection
    if params.fields:
        requested_fields = [field.strip() for field in params.fields.split(",")]
        all_users = [
            model.UserResponse(
                **{
                    field: getattr(user, field)
                    for field in requested_fields
                    if hasattr(user, field)
                }
            )
            for user in all_users
        ]
    # Pagination
    offset = (params.page - 1) * params.limit
    total_count = len(all_users)
    all_users = all_users[params.offset :]
    return {
        "data": all_users[offset : offset + params.limit],
        "meta": {
            "total": total_count,
            "page": params.page,
            "limit": params.limit,
            "offset": params.offset,
            "total_pages": int((total_count - params.offset) / params.limit)
            + 1,
        },
    }


@router.post("/", response_model=model.UserResponse, status_code=201)
def create_user(user: model.UserCreate, db: db_dep, response: Response):
    """Endpoint to create a new user.

    Args:
        user (model.UserCreate): The user data to create.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The created user data.
    """
    return service.create_user(user, db, response)


@router.get(
    "/{id}",
    response_model=model.UserResponse,
    response_model_exclude_unset=True,
    status_code=200,
)
def get_user(
    id: str,
    db: db_dep,
    response: Response,
    params: FieldSelectionParams = Depends(),
):
    """Endpoint to retrieve a user by their user_id.

    Args:
        id (str): The unique identifier of the user.
        db (db_dep): The database session.
        user_token (user_admin_dep): The authenticated user token.
        response (Response): The FastAPI response object to set status codes.
        params (FieldSelectionParams): Query parameters for field selection.

    Returns:
        model.UserResponse: The user data if found.
    """
    user = service.get_user_byid(id, db, response)
    # Field Selection
    if params.fields:
        requested_fields = [field.strip() for field in params.fields.split(",")]
        user = model.UserResponse(
            **{
                field: getattr(user, field)
                for field in requested_fields
                if hasattr(user, field)
            }
        )
    return user


@router.put("/{id}", response_model=model.UserResponse)
def update_user(
    id: str, user: model.UserUpdate, db: db_dep, response: Response
):
    """Endpoint to update an existing user's information.

    Args:
        id (str): The unique identifier of the user to update.
        user (model.UserUpdate): The updated user data.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The updated user data.
    """
    return service.update_user(id, user, db, response)


@router.patch("/{id}", response_model=model.UserResponse, status_code=200)
def patch_user(id: str, user: model.UserPatch, db: db_dep, response: Response):
    """Endpoint to partially update an existing user's information.

    Args:
        id (str): The unique identifier of the user to update.
        user (model.UserPatch): The updated user data.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The updated user data.
    """
    return service.patch_user(id, user, db, response)


@router.delete("/{id}", status_code=204)
def delete_user(id: str, db: db_dep, response: Response):
    """Endpoint to delete a user by their user_id.

    Args:
        id (str): The unique identifier of the user to delete.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        None
    """
    service.delete_user(id, db, response)
