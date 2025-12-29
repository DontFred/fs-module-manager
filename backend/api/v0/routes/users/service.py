"""This module provides services for managing user data.

It includes functions to retrieve, create, update, and delete users
from the database, as well as handle related exceptions and logging.
"""

from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from db.model import User
from utils.dependency.initialization import argon2_hasher
from utils.dependency.initialization import db_dep
from utils.logging.initialization import logging

from . import model


def get_all_users(db: db_dep, response: Response) -> list[model.UserResponse]:
    """Retrieve all users from the database.

    Args:
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        list[model.UserResponse]: A list of all users.
    """
    try:
        users = db.query(User).all()
        response.status_code = status.HTTP_200_OK
        return [
            model.UserResponse(
                user_id=user.user_id,
                name=user.name,
                faculty=user.faculty,
                role=user.role,
            )
            for user in users
        ]
    except Exception as e:
        logging.error(f"Error while retrieving users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def create_user(
    user: model.UserCreate, db: db_dep, response: Response
) -> model.UserResponse:
    """Create a new user in the database.

    Args:
        user (model.UserCreate): The user data to create.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The created user data.

    Raises:
        HTTPException: If the user already exists or the password is not hashed.
    """
    try:
        existing_user = (
            db.query(User).filter(User.user_id == user.user_id).first()
        )
    except Exception as e:
        logging.error(
            f"Database error while checking existing user before create: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred.",
        )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists.",
        )
    try:
        is_not_hash = argon2_hasher.check_needs_rehash(user.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be hashed.",
        )
    if is_not_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be hashed.",
        )
    try:
        new_user = User(
            user_id=user.user_id,
            name=user.name,
            faculty=user.faculty,
            role=user.role,
            password=user.password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        response.status_code = status.HTTP_201_CREATED
        logging.info(f"Created new user with ID: {new_user.user_id}")
        return model.UserResponse(
            user_id=new_user.user_id,
            name=new_user.name,
            faculty=new_user.faculty,
            role=new_user.role,
        )
    except Exception as e:
        db.rollback()
        logging.error(f"Error while adding user to database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def get_user_byid(
    id: str, db: db_dep, response: Response
) -> model.UserResponse:
    """Retrieve a user by their user_id.

    Args:
        id (str): The unique identifier of the user.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The user data if found.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()

    except Exception as e:
        logging.error(f"Error while retrieving user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    response.status_code = status.HTTP_200_OK
    return model.UserResponse(
        user_id=user.user_id,
        name=user.name,
        faculty=user.faculty,
        role=user.role,
    )


def update_user(
    id: str, update_data: model.UserUpdate, db: db_dep, response: Response
) -> model.UserResponse:
    """Update an existing user's data.

    Args:
        id (str): The unique identifier of the user to update.
        update_data (model.UserUpdate): The new user data.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The updated user data.

    Raises:
        HTTPException: If the user is not found or an error occurs.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()
    except Exception as e:
        logging.error(f"Error while retrieving user for update: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    try:
        is_not_hash = argon2_hasher.check_needs_rehash(update_data.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be hashed.",
        )
    if is_not_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be hashed.",
        )
    try:
        user.name = update_data.name
        user.faculty = update_data.faculty
        user.role = update_data.role
        user.password = update_data.password
        db.commit()
        db.refresh(user)
        response.status_code = status.HTTP_200_OK
        logging.info(f"Updated user with ID: {user.user_id}")
        return model.UserResponse(
            user_id=user.user_id,
            name=user.name,
            faculty=user.faculty,
            role=user.role,
        )
    except Exception as e:
        db.rollback()
        logging.error(f"Error while updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def patch_user(
    id: str, update_data: model.UserPatch, db: db_dep, response: Response
) -> model.UserResponse:
    """Partially update a user's data.

    Args:
        id (str): The unique identifier of the user to update.
        update_data (model.UserPatch): The partial user data to update.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Returns:
        model.UserResponse: The updated user data.

    Raises:
        HTTPException: If the user is not found, the password is not hashed, or
        an error occurs.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()
    except Exception as e:
        logging.error(f"Error while retrieving user for patch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    if update_data.password:
        try:
            is_not_hash = argon2_hasher.check_needs_rehash(
                update_data.password
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be hashed.",
            )
        if is_not_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be hashed.",
            )
        user.password = update_data.password
    if update_data.name:
        user.name = update_data.name
    if update_data.faculty:
        user.faculty = update_data.faculty
    if update_data.role:
        user.role = update_data.role
    try:
        db.commit()
        db.refresh(user)
        response.status_code = status.HTTP_200_OK
        logging.info(f"Patched user with ID: {user.user_id}")
        return model.UserResponse(
            user_id=user.user_id,
            name=user.name,
            faculty=user.faculty,
            role=user.role,
        )
    except Exception as e:
        db.rollback()
        logging.error(f"Error while patching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def delete_user(id: str, db: db_dep, response: Response) -> None:
    """Delete a user by their user_id.

    Args:
        id (str): The unique identifier of the user to delete.
        db (db_dep): The database session.
        response (Response): The FastAPI response object to set status codes.

    Raises:
        HTTPException: If the user is not found or an error occurs.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()
    except Exception as e:
        logging.error(f"Error while retrieving user for deletion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    try:
        db.delete(user)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        logging.info(f"Deleted user with ID: {id}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error while deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )
