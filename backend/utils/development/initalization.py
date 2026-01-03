"""This module provides utility functions for development exercises.

It includes functions to reset the database, seed it with initial data,
and create default users.
"""

from sqlalchemy import Engine

from db.model import Base
from utils.logging.initialization import logger


def nuke_pave_seed(engine: Engine):
    """Reset the database, seed it with initial data, and create default users.

    This function initializes the database by removing existing data,
    and then seeds it with predefined user accounts for various roles.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    from utils.dependency.initialization import get_db

    db = next(get_db())

    from .mock.auditlogs import mock_auditlogs
    from .mock.modules import mock_modules
    from .mock.translation import mock_translations
    from .mock.user import mock_user
    from .mock.versions import mock_versions

    try:
        users = mock_user()
        modules = mock_modules(users)
        versions = mock_versions(modules)
        translations = mock_translations(versions)
        auditlogs = mock_auditlogs(versions, users)

        db.add_all(users)
        db.commit()
        db.add_all(modules)
        db.commit()
        db.add_all(versions)
        db.commit()
        db.add_all(translations)
        db.commit()
        db.add_all(auditlogs)
        db.commit()

    except Exception as e:
        logger.error(f"Error while seeding database: {e}")
        db.rollback()
        raise e
