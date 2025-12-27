"""This module handles the initialization of the database.

It includes functions and configurations required to set up the database for
the application.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine

from db.model import Base
from db.model import User

load_dotenv()

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "please_change_me")
DB_DATABASE = os.getenv("DB_DATABASE", "modules")
environment = os.getenv("ENVIRONMENT", "development")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432/{DB_DATABASE}"
)

engine = create_engine(DATABASE_URL, echo=(environment == "development"))


def setup_database(engine: Engine = engine):
    """Set up the database by creating all tables defined in the models."""
    if environment == "development":
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        from utils.dependency.initialization import get_db

        db = next(get_db())
        module_owner_user = User(
            id=1,
            name="module_owner",
            role="MODULE_OWNER",
            password="$2a$12$b7PPIk7O4ruq50Z1iFNkQO0bLAjh3LHzix/K.GxEY8bjL0YMxatQa",
        )
        program_coordinator_user = User(
            id=2,
            name="program_coordinator",
            role="PROGRAM_COORDINATOR",
            password="$2a$12$b7PPIk7O4ruq50Z1iFNkQO0bLAjh3LHzix/K.GxEY8bjL0YMxatQa",
        )
        examination_office_user = User(
            id=3,
            name="examination_office",
            role="EXAMINATION_OFFICE",
            password="$2a$12$b7PPIk7O4ruq50Z1iFNkQO0bLAjh3LHzix/K.GxEY8bjL0YMxatQa",
        )
        deanery_user = User(
            id=4,
            name="deanery",
            role="DEANERY",
            password="$2a$12$b7PPIk7O4ruq50Z1iFNkQO0bLAjh3LHzix/K.GxEY8bjL0YMxatQa",
        )
        admin_user = User(
            id=5,
            name="admin",
            role="ADMIN",
            password="$2a$12$b7PPIk7O4ruq50Z1iFNkQO0bLAjh3LHzix/K.GxEY8bjL0YMxatQa",
        )

        db.add_all(
            [
                module_owner_user,
                program_coordinator_user,
                examination_office_user,
                deanery_user,
                admin_user,
            ]
        )
        db.commit()
    else:
        Base.metadata.create_all(engine)
