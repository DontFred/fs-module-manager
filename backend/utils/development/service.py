"""This module provides utility functions for development exercises.

It includes functions to reset the database, seed it with initial data,
and create default users.
"""

from sqlalchemy import Engine

from db.model import Base
from db.model import Faculty
from db.model import User
from db.model import UserRole
from utils.logging.initialization import logging


def nuke_pave_seed(engine: Engine):
    """Reset the database, seed it with initial data, and create default users.

    This function initializes the database by removing existing data,
    and then seeds it with predefined user accounts for various roles.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    from utils.dependency.initialization import get_db

    db = next(get_db())

    from utils.dependency.initialization import argon2_hasher

    module_owner_f1_user = User(
        user_id=11,
        name="Module Owner Faculty1",
        faculty=Faculty.F1_MPM,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    module_owner_f2_user = User(
        user_id=12,
        name="Module Owner Faculty2",
        faculty=Faculty.F2_ELS,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    module_owner_f3_user = User(
        user_id=13,
        name="Module Owner Faculty3",
        faculty=Faculty.F3_IC,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    module_owner_f4_user = User(
        user_id=14,
        name="Module Owner Faculty4",
        faculty=Faculty.F4_BS,
        role=UserRole.MODULE_OWNER,
        password=argon2_hasher.hash("password"),
    )
    program_coordinator_f1_user = User(
        user_id=21,
        name="Program Coordinator Faculty1",
        faculty=Faculty.F1_MPM,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )
    program_coordinator_f2_user = User(
        user_id=22,
        name="Program Coordinator Faculty2",
        faculty=Faculty.F2_ELS,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )
    program_coordinator_f3_user = User(
        user_id=23,
        name="Program Coordinator Faculty3",
        faculty=Faculty.F3_IC,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )

    program_coordinator_f4_user = User(
        user_id=24,
        name="Program Coordinator Faculty4",
        faculty=Faculty.F4_BS,
        role=UserRole.PROGRAM_COORDINATOR,
        password=argon2_hasher.hash("password"),
    )

    examination_office_user = User(
        user_id=35,
        name="examination_office",
        role=UserRole.EXAMINATION_OFFICE,
        faculty=Faculty.ADMIN,
        password=argon2_hasher.hash("password"),
    )
    deanery_user = User(
        user_id=45,
        name="deanery",
        role=UserRole.DEANERY,
        faculty=Faculty.ADMIN,
        password=argon2_hasher.hash("password"),
    )
    admin_user = User(
        user_id=55,
        name="admin",
        faculty=Faculty.ADMIN,
        role=UserRole.ADMIN,
        password=argon2_hasher.hash("password"),
    )
    try:
        db.add_all(
            [
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
        )
        db.commit()
    except Exception as e:
        logging.error(f"Error while seeding database: {e}")
        db.rollback()
        raise e
