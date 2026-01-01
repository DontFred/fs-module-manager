"""Tests for the /v0/users API endpoint.

This module contains tests to verify the functionality of the /v0/users
endpoint, including retrieving all users and security checks.
"""

from api.model import PaginatedResponse
from api.model import PaginationMeta
from api.v0.routes.users import model
from utils.dependency.initialization import argon2_hasher
from utils.development.mock.user import get_mock_user

mock_user = get_mock_user()


def test_get_all_users(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users", headers=headers)
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


def test_get_all_users_with_filter_faculty_f1(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with faculty=f1."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/users?faculty=F1_MECHANICAL_PROCESS_MARITIME", headers=headers
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


def test_get_all_users_with_filter_faculty_f2(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with faculty=f2."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/users?faculty=F2_ENERGY_LIFE_SCIENCE", headers=headers
    )
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


def test_get_all_users_with_filter_faculty_f3(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with faculty=f3."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/users?faculty=F3_INFORMATION_COMMUNICATION", headers=headers
    )
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


def test_get_all_users_with_filter_faculty_f4(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with faculty=f4."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/users?faculty=F4_BUSINESS_SCHOOL", headers=headers
    )
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


def test_get_all_users_with_filter_faculty_admin(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with faculty=admin."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?faculty=ADMIN", headers=headers)
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


def test_get_all_users_with_filter_role_module_owner(
    test_client, admin_user_login
):
    """Test the /v0/users endpoint to get all users with role=module_owner."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?role=MODULE_OWNER", headers=headers)
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


def test_get_all_users_with_filter_role_program_coordinator(
    test_client, admin_user_login
):
    """Test the /v0/users endpoint to get all users with role=program_coordinator."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/users?role=PROGRAM_COORDINATOR", headers=headers
    )
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


def test_get_all_users_with_filter_role_examination_office(
    test_client, admin_user_login
):
    """Test the /v0/users endpoint to get all users with role=examination_office."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/users?role=EXAMINATION_OFFICE", headers=headers
    )
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


def test_get_all_users_with_filter_role_deanery(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with role=deanery."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?role=DEANERY", headers=headers)
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


def test_get_all_users_with_filter_role_admin(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with role=admin."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?role=ADMIN", headers=headers)
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


def test_get_all_users_with_search_name(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with search name."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    mock_name = mock_user[0].name
    response = test_client.get("/v0/users?search=" + mock_name, headers=headers)
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


def test_get_all_users_with_search_id(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with search id."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    mock_id = mock_user[0].user_id
    response = test_client.get("/v0/users?search=" + mock_id, headers=headers)
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


def test_get_all_users_with_sorting_desc(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with sorting desc."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?sort_order=desc", headers=headers)
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


def test_get_all_users_with_sorting_by_name(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with sorting by name."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?sort_by=name", headers=headers)
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


def test_get_all_users_with_field_selection(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with field selection."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?fields=user_id,name", headers=headers)
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


def test_get_all_users_with_pagination(test_client, admin_user_login):
    """Test the /v0/users endpoint to get all users with pagination."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users?page=2&limit=5", headers=headers)
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


def test_create_user(test_client, admin_user_login):
    """Test the /v0/users endpoint to create a new user."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    new_user = {
        "user_id": "test_user_123",
        "name": "Test User",
        "faculty": "F1_MECHANICAL_PROCESS_MARITIME",
        "role": "MODULE_OWNER",
        "password": argon2_hasher.hash("securepassword"),
    }
    response = test_client.post("/v0/users", json=new_user, headers=headers)
    assert response.status_code == 201
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == new_user["user_id"]
    assert data.name == new_user["name"]
    assert data.faculty == model.Faculty.F1_MPM
    assert data.role == model.UserRole.MODULE_OWNER


def test_create_user_existing_id(test_client, admin_user_login):
    """Test the /v0/users endpoint to create a user with an existing user_id."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    existing_user = {
        "user_id": mock_user[0].user_id,
        "name": "Another User",
        "faculty": "F2_ENERGY_LIFE_SCIENCE",
        "role": "DEANERY",
        "password": argon2_hasher.hash("anotherpassword"),
    }
    response = test_client.post(
        "/v0/users", json=existing_user, headers=headers
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "User already exists."


def test_create_user_unhashed_password(test_client, admin_user_login):
    """Test the /v0/users endpoint to create a user with an unhashed password."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    new_user = {
        "user_id": "test_user_456",
        "name": "Test User 2",
        "faculty": "F3_INFORMATION_COMMUNICATION",
        "role": "PROGRAM_COORDINATOR",
        "password": "plainpassword",
    }
    response = test_client.post("/v0/users", json=new_user, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Password must be hashed."


def test_get_user_by_id(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint to get a user by user_id."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_user = mock_user[0]
    response = test_client.get(
        f"/v0/users/{target_user.user_id}", headers=headers
    )
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == target_user.name
    assert data.faculty == target_user.faculty
    assert data.role == target_user.role


def test_get_user_by_id_not_found(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint for a non-existing user_id."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/users/non_existing_user", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."


def test_get_user_by_id_with_field_selection(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint with field selection."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_user = mock_user[0]
    response = test_client.get(
        f"/v0/users/{target_user.user_id}?fields=user_id,name",
        headers=headers,
    )
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == target_user.name
    assert data.faculty is None
    assert data.role is None


def test_update_user(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint to update a user's details."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_user = mock_user[11]
    updated_data = {
        "name": "Updated Name",
        "faculty": "F4_BUSINESS_SCHOOL",
        "role": "ADMIN",
        "password": argon2_hasher.hash("newsecurepassword"),
    }
    response = test_client.put(
        f"/v0/users/{target_user.user_id}",
        json=updated_data,
        headers=headers,
    )
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == updated_data["name"]
    assert data.faculty == model.Faculty.F4_BS
    assert data.role == model.UserRole.ADMIN


def test_update_user_not_found(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint for updating a non-existing user."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    updated_data = {
        "name": "Non Existing User",
        "faculty": "F1_MECHANICAL_PROCESS_MARITIME",
        "role": "MODULE_OWNER",
        "password": argon2_hasher.hash("somepassword"),
    }
    response = test_client.put(
        "/v0/users/non_existing_user", json=updated_data, headers=headers
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."


def test_update_user_unhashed_password(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint to update a user with an unhashed password."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_user = mock_user[11]
    updated_data = {
        "name": "Updated Name",
        "faculty": "F2_ENERGY_LIFE_SCIENCE",
        "role": "DEANERY",
        "password": "plainpassword",
    }
    response = test_client.put(
        f"/v0/users/{target_user.user_id}",
        json=updated_data,
        headers=headers,
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Password must be hashed."


def test_patch_user(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint to patch a user's details."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_user = mock_user[12]
    patch_data = {
        "name": "Patched Name",
    }
    response = test_client.patch(
        f"/v0/users/{target_user.user_id}",
        json=patch_data,
        headers=headers,
    )
    assert response.status_code == 200
    data = model.UserResponse.model_validate(response.json())
    assert data.user_id == target_user.user_id
    assert data.name == patch_data["name"]
    assert data.faculty == target_user.faculty
    assert data.role == target_user.role


def test_patch_user_not_found(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint for patching a non-existing user."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    patch_data = {
        "name": "Non Existing User",
    }
    response = test_client.patch(
        "/v0/users/non_existing_user", json=patch_data, headers=headers
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."


def test_patch_user_unhashed_password(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint to patch a user with an unhashed password."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_user = mock_user[12]
    patch_data = {
        "password": "plainpassword",
    }
    response = test_client.patch(
        f"/v0/users/{target_user.user_id}",
        json=patch_data,
        headers=headers,
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Password must be hashed."


def test_delete_user(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint to delete a user."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_user = mock_user[13]
    response = test_client.delete(
        f"/v0/users/{target_user.user_id}", headers=headers
    )
    assert response.status_code == 204
    # Verify the user is deleted
    get_response = test_client.get(
        f"/v0/users/{target_user.user_id}", headers=headers
    )
    assert get_response.status_code == 404


def test_delete_user_not_found(test_client, admin_user_login):
    """Test the /v0/users/{user_id} endpoint for deleting a non-existing user."""  # noqa: E501
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.delete(
        "/v0/users/non_existing_user", headers=headers
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found."


# --------------------------------------------------------------------------
# AUTHENTICATION TESTS
# --------------------------------------------------------------------------


def test_get_all_users_unauthorized(test_client):
    """Test the /v0/users endpoint without authorization header."""
    response = test_client.get("/v0/users")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_user_unauthorized(test_client):
    """Test create user endpoint without authorization header."""
    new_user = {
        "user_id": "auth_test_user",
        "name": "Auth Test",
        "faculty": "F1_MECHANICAL_PROCESS_MARITIME",
        "role": "MODULE_OWNER",
        "password": argon2_hasher.hash("password"),
    }
    response = test_client.post("/v0/users", json=new_user)
    assert response.status_code == 401


def test_create_user_insufficient_permissions(test_client, f1_mo_user_login):
    """Test create user endpoint with a non-admin user (Module Owner)."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}
    new_user = {
        "user_id": "auth_test_user_2",
        "name": "Auth Test 2",
        "faculty": "F1_MECHANICAL_PROCESS_MARITIME",
        "role": "MODULE_OWNER",
        "password": argon2_hasher.hash("password"),
    }
    response = test_client.post("/v0/users", json=new_user, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not enough permissions"


def test_get_user_by_id_unauthorized(test_client):
    """Test get user by ID endpoint without authorization header."""
    target_user = mock_user[0]
    response = test_client.get(f"/v0/users/{target_user.user_id}")
    assert response.status_code == 401


def test_update_user_unauthorized(test_client):
    """Test update user endpoint without authorization header."""
    target_user = mock_user[11]
    updated_data = {
        "name": "Updated Fail Name",
        "faculty": "F4_BUSINESS_SCHOOL",
        "role": "ADMIN",
        "password": argon2_hasher.hash("newsecurepassword"),
    }
    response = test_client.put(
        f"/v0/users/{target_user.user_id}", json=updated_data
    )
    assert response.status_code == 401


def test_update_user_insufficient_permissions(test_client, f1_mo_user_login):
    """Test update user endpoint with a non-admin user (Module Owner)."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}
    target_user = mock_user[11]
    updated_data = {
        "name": "Updated Fail Name",
        "faculty": "F4_BUSINESS_SCHOOL",
        "role": "ADMIN",
        "password": argon2_hasher.hash("newsecurepassword"),
    }
    response = test_client.put(
        f"/v0/users/{target_user.user_id}",
        json=updated_data,
        headers=headers,
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not enough permissions"


def test_patch_user_unauthorized(test_client):
    """Test patch user endpoint without authorization header."""
    target_user = mock_user[12]
    patch_data = {"name": "Unauthorized Patch"}
    response = test_client.patch(
        f"/v0/users/{target_user.user_id}", json=patch_data
    )
    assert response.status_code == 401


def test_patch_user_insufficient_permissions(test_client, f1_mo_user_login):
    """Test patch user endpoint with a non-admin user (Module Owner)."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}
    target_user = mock_user[12]
    patch_data = {"name": "Forbidden Patch"}
    response = test_client.patch(
        f"/v0/users/{target_user.user_id}",
        json=patch_data,
        headers=headers,
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not enough permissions"


def test_delete_user_unauthorized(test_client):
    """Test delete user endpoint without authorization header."""
    target_user = mock_user[13]
    response = test_client.delete(f"/v0/users/{target_user.user_id}")
    assert response.status_code == 401


def test_delete_user_insufficient_permissions(test_client, f1_mo_user_login):
    """Test delete user endpoint with a non-admin user (Module Owner)."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}
    target_user = mock_user[13]
    response = test_client.delete(
        f"/v0/users/{target_user.user_id}", headers=headers
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not enough permissions"
