"""This module defines the API endpoints for user-related operations.

It includes endpoints for:
- Retrieving all users
- Creating a new user
- Retrieving a user by ID
- Updating a user's information
- Deleting a user
"""

from fastapi import APIRouter
from fastapi import Response

from utils.dependency.initialization import db_dep

from . import model
from . import service

router = APIRouter(prefix="/v0/users", tags=["Users"])


@router.get("/", response_model=list[model.UserResponse])
def get_users(db: db_dep, response: Response):
    """Endpoint to retrieve a list of all users.

    Args:
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        list[model.UserResponse]: A list of user data.
    """
    return service.get_all_users(db, response)


@router.post("/", response_model=model.UserResponse)
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


@router.get("/{id}", response_model=model.UserResponse)
def get_user(id: str, db: db_dep, response: Response):
    """Endpoint to retrieve a user by their user_id.

    Args:
        id (str): The unique identifier of the user.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The user data if found.
    """
    return service.get_user_byid(id, db, response)


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
