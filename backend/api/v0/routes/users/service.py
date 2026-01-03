"""This module provides services for managing user data.

It includes functions to retrieve, create, update, and delete users
from the database, as well as handle related exceptions and logging.
"""

from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy import or_

from api.model import FieldSelectionParams
from api.model import PaginatedResponse
from db.model import User
from utils.dependency.initialization import argon2_hasher
from utils.dependency.initialization import db_dep
from utils.logging.initialization import logger

from . import model


def get_all_users(
    db: db_dep, response: Response, params: model.AllUsersQueryParams
) -> PaginatedResponse[model.UserResponse]:
    """Retrieve all users based on query parameters.

    Parameters:
    ----------
    db : db_dep
        The database dependency for querying users.
    response : Response
        The HTTP response object.
    params : model.AllUsersQueryParams
        The query parameters for filtering, sorting, and pagination.

    Returns:
    -------
    PaginatedResponse[model.UserResponse]
        A paginated response containing user data matching the query parameters.

    Raises:
    ------
    HTTPException
        If an error occurs during the retrieval process.
    """
    try:
        query = db.query(User)

        if params.faculty:
            query = query.filter(User.faculty == params.faculty)

        if params.role:
            query = query.filter(User.role == params.role)

        if params.search:
            query = query.filter(
                or_(
                    User.name.ilike(f"%{params.search}%"),
                    User.user_id.ilike(f"%{params.search}%"),
                )
            )

        match params.sort_by:
            case model.UserFields.USER_ID:
                sort_column = User.user_id
            case model.UserFields.NAME:
                sort_column = User.name
            case model.UserFields.FACULTY:
                sort_column = User.faculty
            case model.UserFields.ROLE:
                sort_column = User.role
            case _:
                sort_column = None
        if sort_column:
            if params.sort_order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

        skip = (
            params.offset
            if params.offset > 0
            else ((params.page - 1) * params.limit)
        )
        total_items = query.count()
        query = query.offset(skip).limit(params.limit)

        users = query.all()

        response.status_code = status.HTTP_200_OK
        response_data = []
        if params.fields:
            for user in users:
                requested_fields = [
                    field.strip() for field in params.fields.split(",")
                ]
                user = model.UserResponse(
                    **{
                        field: getattr(user, field)
                        for field in requested_fields
                        if hasattr(user, field)
                    }
                )
                response_data.append(user)
        else:
            response_data = [
                model.UserResponse(
                    user_id=user.user_id,
                    name=user.name,
                    faculty=user.faculty,
                    role=user.role,
                )
                for user in users
            ]
        return PaginatedResponse[model.UserResponse](
            data=response_data,
            meta={
                "total": total_items,
                "page": params.page,
                "limit": params.limit,
                "offset": params.offset,
                "total_pages": int((total_items - params.offset) / params.limit)
                + 1,
            },
        )
    except Exception as e:
        logger.error(f"Error while retrieving users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def create_user(
    user: model.UserCreate, db: db_dep, response: Response
) -> model.UserResponse:
    """Create a new user in the database.

    Parameters:
    ----------
    user : model.UserCreate
        The user data to create a new user.
    db : db_dep
        The database dependency for querying and adding the user.
    response : Response
        The HTTP response object.

    Returns:
    -------
    model.UserResponse
        The created user data.

    Raises:
    ------
    HTTPException
        If the user already exists, the password is not hashed, or an error
        occurs during the creation process.
    """
    try:
        existing_user = (
            db.query(User).filter(User.user_id == user.user_id).first()
        )
    except Exception as e:
        logger.error(
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
        return model.UserResponse(
            user_id=new_user.user_id,
            name=new_user.name,
            faculty=new_user.faculty,
            role=new_user.role,
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error while adding user to database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def get_user_byid(
    id: str, db: db_dep, response: Response, params: FieldSelectionParams
) -> model.UserResponse:
    """Retrieve a user by their ID.

    Parameters:
    ----------
    id : str
        The unique identifier of the user.
    db : db_dep
        The database dependency for querying the user.
    response : Response
        The HTTP response object.
    params : FieldSelectionParams
        Parameters for selecting specific fields in the response.

    Returns:
    -------
    model.UserResponse
        The user data matching the given ID.

    Raises:
    ------
    HTTPException
        If the user is not found or an error occurs during retrieval.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()

    except Exception as e:
        logger.error(f"Error while retrieving user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    response.status_code = status.HTTP_200_OK

    user = model.UserResponse(
        user_id=user.user_id,
        name=user.name,
        faculty=user.faculty,
        role=user.role,
    )

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


def update_user(
    id: str, update_data: model.UserUpdate, db: db_dep, response: Response
) -> model.UserResponse:
    """Update an existing user's information.

    Parameters
    ----------
    id : str
        The unique identifier of the user to be updated.
    update_data : model.UserUpdate
        The data to update the user with.
    db : db_dep
        The database dependency for querying and updating the user.
    response : Response
        The HTTP response object.

    Returns:
    -------
    model.UserResponse
        The updated user data.

    Raises:
    ------
    HTTPException
        If the user is not found, the password is not hashed, or an error occurs
        during the update process.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()
    except Exception as e:
        logger.error(f"Error while retrieving user for update: {e}")
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
        return model.UserResponse(
            user_id=user.user_id,
            name=user.name,
            faculty=user.faculty,
            role=user.role,
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error while updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def patch_user(
    id: str, update_data: model.UserPatch, db: db_dep, response: Response
) -> model.UserResponse:
    """Partially update an existing user's information.

    Parameters:
    ----------
    id : str
        The unique identifier of the user to be updated.
    update_data : model.UserPatch
        The data to partially update the user with.
    db : db_dep
        The database dependency for querying and updating the user.
    response : Response
        The HTTP response object.

    Returns:
    -------
    model.UserResponse
        The updated user data.

    Raises:
    ------
    HTTPException
        If the user is not found, the password is not hashed, or an error occurs
        during the update process.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()
    except Exception as e:
        logger.error(f"Error while retrieving user for patch: {e}")
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
        return model.UserResponse(
            user_id=user.user_id,
            name=user.name,
            faculty=user.faculty,
            role=user.role,
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error while patching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )


def delete_user(id: str, db: db_dep, response: Response) -> None:
    """Delete a user by their ID.

    Parameters
    ----------
    id : str
        The unique identifier of the user to be deleted.
    db : db_dep
        The database dependency for querying and deleting the user.
    response : Response
        The HTTP response object.

    Raises:
    ------
    HTTPException
        If the user is not found or an error occurs during the deletion process.
    """
    try:
        user = db.query(User).filter(User.user_id == id).first()
    except Exception as e:
        logger.error(f"Error while retrieving user for deletion: {e}")
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
    except Exception as e:
        db.rollback()
        logger.error(f"Error while deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred.",
        )
