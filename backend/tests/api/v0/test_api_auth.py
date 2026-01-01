"""Tests for the authentication API endpoints.

This module contains tests to verify the functionality of the authentication
endpoints, including login with various user roles and error handling for
incorrect credentials.
"""


def test_login_for_access_token_wrong_credentials(test_client):
    """Test login with wrong credentials to ensure proper error handling."""
    response = test_client.post(
        "/v0/auth/token",
        data={"username": "wrong_user", "password": "wrong_pass"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect user_id or password."}
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_f1_mo_user_login_for_access_token(f1_mo_user_login):
    """Test login for f1 module owner user."""
    assert f1_mo_user_login is not None


def test_f2_mo_user_login_for_access_token(f2_mo_user_login):
    """Test login for f2 module owner user."""
    assert f2_mo_user_login is not None


def test_f3_mo_user_login_for_access_token(f3_mo_user_login):
    """Test login for f3 module owner user."""
    assert f3_mo_user_login is not None


def test_f4_mo_user_login_for_access_token(f4_mo_user_login):
    """Test login for f4 module owner user."""
    assert f4_mo_user_login is not None


def test_f1_pc_user_login_for_access_token(f1_pc_user_login):
    """Test login for f1 program coordinator user."""
    assert f1_pc_user_login is not None


def test_f2_pc_user_login_for_access_token(f2_pc_user_login):
    """Test login for f2 program coordinator user."""
    assert f2_pc_user_login is not None


def test_f3_pc_user_login_for_access_token(f3_pc_user_login):
    """Test login for f3 program coordinator user."""
    assert f3_pc_user_login is not None


def test_f4_pc_user_login_for_access_token(f4_pc_user_login):
    """Test login for f4 program coordinator user."""
    assert f4_pc_user_login is not None


def test_examination_office_user_login_for_access_token(
    eo_user_login,
):
    """Test login for examination office user."""
    assert eo_user_login is not None


def test_deanery_user_login_for_access_token(deanery_user_login):
    """Test login for deanery user."""
    assert deanery_user_login is not None


def test_admin_user_login_for_access_token(admin_user_login):
    """Test login for admin user."""
    assert admin_user_login is not None
