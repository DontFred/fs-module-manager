"""This module contains fixtures and configurations for pytest.

Fixtures defined here are shared across multiple test modules.
"""
import pytest
from fastapi.testclient import TestClient

from api.initialization import app


@pytest.fixture
def test_client():
    """Provides a TestClient for testing the FastAPI application."""
    with TestClient(app) as client:
        yield client
