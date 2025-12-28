"""This module provides utility functions for development exercises.

It includes functions to reset the database, seed it with initial data,
and create default users.
"""

from sqlalchemy import Engine

from db.model import Base
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

    from .mock.user import mock_user

    users = mock_user()

    try:
        db.add_all(
            users
        )
        db.commit()
    except Exception as e:
        logging.error(f"Error while seeding database: {e}")
        db.rollback()
        raise e
