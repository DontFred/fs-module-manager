"""Tests for the /v0/users API endpoint.

This module contains tests to verify the functionality of the /v0/users
endpoint, including retrieving all users.
"""

from api.model import PaginatedResponse
from api.model import PaginationMeta
from api.v0.routes.users import model
from utils.dependency.initialization import argon2_hasher
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


def test_get_all_users_with_filter_faculty_f1(test_client):
    """Test the /v0/users endpoint to get all users with faculty=f1."""
    response = test_client.get(
        "/v0/users?faculty=F1_MECHANICAL_PROCESS_MARITIME"
    )
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.faculty == model.Faculty.F1_MPM
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_faculty_f2(test_client):
    """Test the /v0/users endpoint to get all users with faculty=f2."""
    response = test_client.get("/v0/users?faculty=F2_ENERGY_LIFE_SCIENCE")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.faculty == model.Faculty.F2_ELS
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_faculty_f3(test_client):
    """Test the /v0/users endpoint to get all users with faculty=f3."""
    response = test_client.get("/v0/users?faculty=F3_INFORMATION_COMMUNICATION")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.faculty == model.Faculty.F3_IC
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_faculty_f4(test_client):
    """Test the /v0/users endpoint to get all users with faculty=f4."""
    response = test_client.get("/v0/users?faculty=F4_BUSINESS_SCHOOL")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.faculty == model.Faculty.F4_BS
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_faculty_admin(test_client):
    """Test the /v0/users endpoint to get all users with faculty=admin."""
    response = test_client.get("/v0/users?faculty=ADMIN")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.faculty == model.Faculty.ADMIN
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_role_module_owner(test_client):
    """Test the /v0/users endpoint to get all users with role=module_owner."""
    response = test_client.get("/v0/users?role=MODULE_OWNER")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.role == model.UserRole.MODULE_OWNER
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_role_program_coordinator(test_client):
    """Test the /v0/users endpoint to get all users with role=program_coordinator."""  # noqa: E501
    response = test_client.get("/v0/users?role=PROGRAM_COORDINATOR")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user
        for user in mock_user
        if user.role == model.UserRole.PROGRAM_COORDINATOR
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_role_examination_office(test_client):
    """Test the /v0/users endpoint to get all users with role=examination_office."""  # noqa: E501
    response = test_client.get("/v0/users?role=EXAMINATION_OFFICE")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user
        for user in mock_user
        if user.role == model.UserRole.EXAMINATION_OFFICE
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_role_deanery(test_client):
    """Test the /v0/users endpoint to get all users with role=deanery."""
    response = test_client.get("/v0/users?role=DEANERY")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.role == model.UserRole.DEANERY
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_filter_role_admin(test_client):
    """Test the /v0/users endpoint to get all users with role=admin."""
    response = test_client.get("/v0/users?role=ADMIN")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user for user in mock_user if user.role == model.UserRole.ADMIN
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_search_name(test_client):
    """Test the /v0/users endpoint to get all users with search name."""
    mock_name = mock_user[0].name
    response = test_client.get("/v0/users?search=" + mock_name)
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user
        for user in mock_user
        if mock_name in user.name or mock_name in user.user_id
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_search_id(test_client):
    """Test the /v0/users endpoint to get all users with search id."""
    mock_id = mock_user[0].user_id
    response = test_client.get("/v0/users?search=" + mock_id)
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    filtered_users = [
        user
        for user in mock_user
        if mock_id in user.name or mock_id in user.user_id
    ]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in filtered_users
        ],
        meta=PaginationMeta(
            total=len(filtered_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(filtered_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_sorting_desc(test_client):
    """Test the /v0/users endpoint to get all users with sorting desc."""
    response = test_client.get("/v0/users?sort_order=desc")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    sorted_users = sorted(
        mock_user,
        key=lambda user: getattr(user, "user_id"),
        reverse=True,
    )
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in sorted_users
        ],
        meta=PaginationMeta(
            total=len(sorted_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(sorted_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_sorting_by_name(test_client):
    """Test the /v0/users endpoint to get all users with sorting by name."""
    response = test_client.get("/v0/users?sort_by=name")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    sorted_users = sorted(
        mock_user,
        key=lambda user: getattr(user, "name"),
        reverse=False,
    )
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in sorted_users
        ],
        meta=PaginationMeta(
            total=len(sorted_users),
            page=1,
            limit=50,
            offset=0,
            total_pages=int(len(sorted_users) / 50) + 1,
        ),
    )

    assert data == exceptdata


def test_get_all_users_with_field_selection(test_client):
    """Test the /v0/users endpoint to get all users with field selection."""
    response = test_client.get("/v0/users?fields=user_id,name")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(
                user_id=user.user_id,
                name=user.name,
            )
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


def test_get_all_users_with_pagination(test_client):
    """Test the /v0/users endpoint to get all users with pagination."""
    response = test_client.get("/v0/users?page=2&limit=5")
    assert response.status_code == 200
    data = PaginatedResponse[model.UserResponse].model_validate(response.json())
    offset = (2 - 1) * 5
    paginated_users = mock_user[offset : offset + 5]
    exceptdata = PaginatedResponse[model.UserResponse](
        data=[
            model.UserResponse(**user.model_dump(exclude={"password"}))
            for user in paginated_users
        ],
        meta=PaginationMeta(
            total=len(mock_user),
            page=2,
            limit=5,
            offset=0,
            total_pages=int(len(mock_user) / 5) + 1,
        ),
    )

    assert data == exceptdata


def test_create_user(test_client):
    """Test the /v0/users endpoint to create a new user."""
    new_user = {
        "user_id": "test_user_123",
        "name": "Test User",
        "faculty": "F1_MECHANICAL_PROCESS_MARITIME",
        "role": "MODULE_OWNER",
        "password": argon2_hasher.hash("securepassword"),
    }
    response = test_client.post("/v0/users", json=new_user)
    assert response.status_code == 201
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == new_user["user_id"]
    assert data.name == new_user["name"]
    assert data.faculty == model.Faculty.F1_MPM
    assert data.role == model.UserRole.MODULE_OWNER


def test_create_user_existing_id(test_client):
    """Test the /v0/users endpoint to create a user with an existing user_id."""
    existing_user = {
        "user_id": mock_user[0].user_id,
        "name": "Another User",
        "faculty": "F2_ENERGY_LIFE_SCIENCE",
        "role": "DEANERY",
        "password": argon2_hasher.hash("anotherpassword"),
    }
    response = test_client.post("/v0/users", json=existing_user)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "User already exists."


def test_create_user_unhashed_password(test_client):
    """Test the /v0/users endpoint to create a user with an unhashed password."""  # noqa: E501
    new_user = {
        "user_id": "test_user_456",
        "name": "Test User 2",
        "faculty": "F3_INFORMATION_COMMUNICATION",
        "role": "PROGRAM_COORDINATOR",
        "password": "plainpassword",
    }
    response = test_client.post("/v0/users", json=new_user)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Password must be hashed."


def test_get_user_by_id(test_client):
    """Test the /v0/users/{user_id} endpoint to get a user by user_id."""
    target_user = mock_user[0]
    response = test_client.get(f"/v0/users/{target_user.user_id}")
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == target_user.name
    assert data.faculty == target_user.faculty
    assert data.role == target_user.role


def test_get_user_by_id_not_found(test_client):
    """Test the /v0/users/{user_id} endpoint for a non-existing user_id."""
    response = test_client.get("/v0/users/non_existing_user")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."


def test_get_user_by_id_with_field_selection(test_client):
    """Test the /v0/users/{user_id} endpoint with field selection."""
    target_user = mock_user[0]
    response = test_client.get(
        f"/v0/users/{target_user.user_id}?fields=user_id,name"
    )
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == target_user.name
    assert data.faculty is None
    assert data.role is None


def test_update_user(test_client):
    """Test the /v0/users/{user_id} endpoint to update a user's details."""
    target_user = mock_user[0]
    updated_data = {
        "name": "Updated Name",
        "faculty": "F4_BUSINESS_SCHOOL",
        "role": "ADMIN",
        "password": argon2_hasher.hash("newsecurepassword"),
    }
    response = test_client.put(
        f"/v0/users/{target_user.user_id}", json=updated_data
    )
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == updated_data["name"]
    assert data.faculty == model.Faculty.F4_BS
    assert data.role == model.UserRole.ADMIN


def test_update_user_not_found(test_client):
    """Test the /v0/users/{user_id} endpoint for updating a non-existing user."""  # noqa: E501
    updated_data = {
        "name": "Non Existing User",
        "faculty": "F1_MECHANICAL_PROCESS_MARITIME",
        "role": "MODULE_OWNER",
        "password": argon2_hasher.hash("somepassword"),
    }
    response = test_client.put("/v0/users/non_existing_user", json=updated_data)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."


def test_update_user_unhashed_password(test_client):
    """Test the /v0/users/{user_id} endpoint to update a user with an unhashed password."""  # noqa: E501
    target_user = mock_user[0]
    updated_data = {
        "name": "Updated Name",
        "faculty": "F2_ENERGY_LIFE_SCIENCE",
        "role": "DEANERY",
        "password": "plainpassword",
    }
    response = test_client.put(
        f"/v0/users/{target_user.user_id}", json=updated_data
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Password must be hashed."


def test_patch_user(test_client):
    """Test the /v0/users/{user_id} endpoint to patch a user's details."""
    target_user = mock_user[1]
    patch_data = {
        "name": "Patched Name",
    }
    response = test_client.patch(
        f"/v0/users/{target_user.user_id}", json=patch_data
    )
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == patch_data["name"]
    assert data.faculty == target_user.faculty
    assert data.role == target_user.role


def test_patch_user_not_found(test_client):
    """Test the /v0/users/{user_id} endpoint for patching a non-existing user."""  # noqa: E501
    patch_data = {
        "name": "Non Existing User",
    }
    response = test_client.patch("/v0/users/non_existing_user", json=patch_data)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."


def test_patch_user_unhashed_password(test_client):
    """Test the /v0/users/{user_id} endpoint to patch a user with an unhashed password."""  # noqa: E501
    target_user = mock_user[1]
    patch_data = {
        "password": "plainpassword",
    }
    response = test_client.patch(
        f"/v0/users/{target_user.user_id}", json=patch_data
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Password must be hashed."


def test_delete_user(test_client):
    """Test the /v0/users/{user_id} endpoint to delete a user."""
    target_user = mock_user[2]
    response = test_client.delete(f"/v0/users/{target_user.user_id}")
    assert response.status_code == 204
    # Verify the user is deleted
    get_response = test_client.get(f"/v0/users/{target_user.user_id}")
    assert get_response.status_code == 404


def test_delete_user_not_found(test_client):
    """Test the /v0/users/{user_id} endpoint for deleting a non-existing user."""  # noqa: E501
    response = test_client.delete("/v0/users/non_existing_user")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."
