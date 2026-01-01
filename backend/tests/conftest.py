"""This module contains fixtures and configurations for pytest.

Fixtures defined here are shared across multiple test modules.
"""

import pytest
from fastapi.testclient import TestClient

from api.initialization import app
from api.v0.routes.auth.model import Token
from db.initialization import setup_database
from db.model import Faculty
from db.model import UserRole
from utils.development.mock.user import get_mock_user
from utils.development.mock.user import password


@pytest.fixture(scope="module")
def test_client():
    """Provides a TestClient for testing the FastAPI application."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def setup() -> None:
    """Setup actions before any tests are run."""
    setup_database()


## Fixtures for different user roles to obtain authentication tokens

mock_user = get_mock_user()


def _login_user(client, role: UserRole, faculty: Faculty):
    user_obj = next(
        user
        for user in mock_user
        if user.role == role and user.faculty == faculty
    )
    response = client.post(
        "/v0/auth/token",
        data={"username": user_obj.user_id, "password": password},
    )
    token_data = Token.model_validate(response.json())
    return token_data.access_token


@pytest.fixture(scope="module")
def f1_mo_user_login(test_client):
    """Fixture to log in as a Module Owner for Faculty F1_MPM.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.MODULE_OWNER, Faculty.F1_MPM)


@pytest.fixture(scope="module")
def f2_mo_user_login(test_client):
    """Fixture to log in as a Module Owner for Faculty F2_ELS.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.MODULE_OWNER, Faculty.F2_ELS)


@pytest.fixture(scope="module")
def f3_mo_user_login(test_client):
    """Fixture to log in as a Module Owner for Faculty F3_IC.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.MODULE_OWNER, Faculty.F3_IC)


@pytest.fixture(scope="module")
def f4_mo_user_login(test_client):
    """Fixture to log in as a Module Owner for Faculty F4_BS.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.MODULE_OWNER, Faculty.F4_BS)


@pytest.fixture(scope="module")
def f1_pc_user_login(test_client):
    """Fixture to log in as a Program Coordinator for Faculty F1_MPM.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(
        test_client, UserRole.PROGRAM_COORDINATOR, Faculty.F1_MPM
    )


@pytest.fixture(scope="module")
def f2_pc_user_login(test_client):
    """Fixture to log in as a Program Coordinator for Faculty F2_ELS.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(
        test_client, UserRole.PROGRAM_COORDINATOR, Faculty.F2_ELS
    )


@pytest.fixture(scope="module")
def f3_pc_user_login(test_client):
    """Fixture to log in as a Program Coordinator for Faculty F3_IC.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.PROGRAM_COORDINATOR, Faculty.F3_IC)


@pytest.fixture(scope="module")
def f4_pc_user_login(test_client):
    """Fixture to log in as a Program Coordinator for Faculty F4_BS.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.PROGRAM_COORDINATOR, Faculty.F4_BS)


@pytest.fixture(scope="module")
def eo_user_login(test_client):
    """Fixture to log in as an Examination Office user.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.EXAMINATION_OFFICE, Faculty.ADMIN)


@pytest.fixture(scope="module")
def deanery_user_login(test_client):
    """Fixture to log in as a Deanery user.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.DEANERY, Faculty.ADMIN)


@pytest.fixture(scope="module")
def admin_user_login(test_client):
    """Fixture to log in as an Admin user.

    Parameters
    ----------
    test_client : TestClient
        The test client used to interact with the FastAPI application.

    Returns:
    -------
    str
        The authentication token for the logged-in user.
    """
    return _login_user(test_client, UserRole.ADMIN, Faculty.ADMIN)
