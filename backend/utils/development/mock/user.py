"""This module provides utilities for creating and managing mock user data.

It includes:
- UserSchema: A Pydantic schema for user validation.
- mock_user: A function to generate mock User objects for testing.
- get_mock_user: A function to retrieve mock users as UserSchema objects.
"""

from pydantic import BaseModel
from pydantic import ConfigDict

from db.model import Faculty
from db.model import User
from db.model import UserRole


class UserSchema(BaseModel):
    """A schema representing a user.

    Attributes:
    ----------
    user_id : str
        The unique identifier for the user.
    name : str
        The name of the user.
    faculty : Faculty
        The faculty to which the user belongs.
    role : UserRole
        The role assigned to the user.
    password : str
        The hashed password of the user.
    """

    user_id: str
    name: str
    faculty: Faculty
    role: UserRole
    password: str
    model_config = ConfigDict(from_attributes=True)

def mock_user():
    """Create and return a list of mock User objects.

    This function generates a predefined set of User objects with
    various roles, faculties, and hashed passwords for development
    and testing purposes.

    Returns:
    -------
    list[User]
        A list of mock User objects.
    """
    from utils.dependency.initialization import argon2_hasher

    module_owner_f1_user = User(
        user_id="11",
        name="Module Owner Faculty1",
        faculty=Faculty.F1_MPM,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    module_owner_f2_user = User(
        user_id="12",
        name="Module Owner Faculty2",
        faculty=Faculty.F2_ELS,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    module_owner_f3_user = User(
        user_id="13",
        name="Module Owner Faculty3",
        faculty=Faculty.F3_IC,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    module_owner_f4_user = User(
        user_id="14",
        name="Module Owner Faculty4",
        faculty=Faculty.F4_BS,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    program_coordinator_f1_user = User(
        user_id="21",
        name="Program Coordinator Faculty1",
        faculty=Faculty.F1_MPM,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )
    program_coordinator_f2_user = User(
        user_id="22",
        name="Program Coordinator Faculty2",
        faculty=Faculty.F2_ELS,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )
    program_coordinator_f3_user = User(
        user_id="23",
        name="Program Coordinator Faculty3",
        faculty=Faculty.F3_IC,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )

    program_coordinator_f4_user = User(
        user_id="24",
        name="Program Coordinator Faculty4",
        faculty=Faculty.F4_BS,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )

    examination_office_user = User(
        user_id="35",
        name="Examination Office",
        role=UserRole.EXAMINATION_OFFICE,
        faculty=Faculty.ADMIN,
        password=argon2_hasher.hash("password"),
    )
    deanery_user = User(
        user_id="45",
        name="Deanery",
        role=UserRole.DEANERY,
        faculty=Faculty.ADMIN,
        password=argon2_hasher.hash("password"),
    )
    admin_user = User(
        user_id="55",
        name="Admin",
        faculty=Faculty.ADMIN,
        role=UserRole.ADMIN,
        password=argon2_hasher.hash("password"),
    )

    return [
        module_owner_f1_user,
        module_owner_f2_user,
        module_owner_f3_user,
        module_owner_f4_user,
        program_coordinator_f1_user,
        program_coordinator_f2_user,
        program_coordinator_f3_user,
        program_coordinator_f4_user,
        examination_office_user,
        deanery_user,
        admin_user,
    ]

def get_mock_user() -> list[UserSchema]:
    """Generate and return a list of mock user data as UserSchema objects.

    This function converts mock User objects into UserSchema objects
    for validation and testing purposes.

    Returns:
    -------
    list[UserSchema]
        A list of validated UserSchema objects.
    """
    return [UserSchema.model_validate(user) for user in mock_user()]
