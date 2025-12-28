"""This module contains fixtures and configurations for pytest.

Fixtures defined here are shared across multiple test modules.
"""

import pytest
from fastapi.testclient import TestClient

from api.initialization import app
from db.initialization import setup_database


@pytest.fixture
def test_client():
    """Provides a TestClient for testing the FastAPI application."""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def setup() -> None:
    """Setup actions before any tests are run."""
    setup_database()


