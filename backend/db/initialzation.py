"""This module handles the initialization of the database.

It includes functions and configurations required to set up the database for
the application.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "please_change_me")
DB_DATABASE = os.getenv("DB_DATABASE", "modules")
environment = os.getenv("ENVIRONMENT", "development")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432/{DB_DATABASE}"

engine = create_engine(DATABASE_URL, echo=(environment == "development"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Get a database session.

    This function provides a database session for interacting with the
    database. It ensures that the session is properly closed after use.

    Yields:
    -------
    Session
        A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

