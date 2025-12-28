"""Tests for the /v0/users API endpoint.

This module contains tests to verify the functionality of the /v0/users
endpoint, including retrieving all users.
"""

from api.model import PaginatedResponse
from api.model import PaginationMeta
from api.v0.routes.users import model
from utils.development.mock.user import get_mock_user

mock_user = get_mock_user()


def test_get_all_users(test_client):
    """Test the /v0/users endpoint to get all users."""
    response = test_client.get("/v0/users")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in mock_user
        ],
        meta=PaginationMeta(
            total=len(mock_user),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(mock_user) / 50) + 1,
        ),
    )

    assert data == exceptdata
