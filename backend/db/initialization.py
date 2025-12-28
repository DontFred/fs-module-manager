"""This module handles the initialization of the database.

It includes functions and configurations required to set up the database for
the application.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine

from db.model import Base

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
        from utils.development.service import nuke_pave_seed

        try:
            nuke_pave_seed(engine)
        except Exception as e:
            print(f"Error during development database setup: {e}")
    else:
        Base.metadata.create_all(engine)
