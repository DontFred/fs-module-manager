"""This module handles the initialization of the database.

It includes functions and configurations required to set up the database for
the application.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine

from db.model import Base
from utils.logging.initialization import logger

load_dotenv()

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "please_change_me")
DB_DATABASE = os.getenv("DB_DATABASE", "modules")
environment = os.getenv("ENVIRONMENT", "development")

if environment == "development":
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432/{DB_DATABASE}"
    )
else:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@db:5432/{DB_DATABASE}"

engine = create_engine(DATABASE_URL, echo=(environment == "development"))


def setup_database(engine: Engine = engine):
    """Set up the database by creating all tables defined in the models."""
    if environment == "development":
        from utils.development.initalization import nuke_pave_seed

        try:
            nuke_pave_seed(engine)
        except Exception as e:
            logger.error(f"Error during development database setup: {e}")
    else:
        Base.metadata.create_all(engine)
