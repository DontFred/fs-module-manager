"""Tests for the /v0/modules API endpoint.

This module contains comprehensive tests for module management, including
retrieval, creation, version control, and workflow status transitions across
different user roles.
"""

import uuid

from api.model import PaginatedResponse
from api.v0.routes.modules import model
from db.model import WorkflowStatus
from utils.development.mock.modules import get_mock_modules
from utils.development.mock.user import get_mock_user
from utils.development.mock.versions import get_mock_versions

mock_modules_data = get_mock_modules()
mock_users_data = get_mock_user()
mock_versions_data = get_mock_versions()


def test_get_all_modules_admin(test_client, admin_user_login):
    """Test retrieving all modules as an admin (sees all statuses)."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get("/v0/modules", headers=headers)
    assert response.status_code == 200
    data = PaginatedResponse[model.ModuleResponse].model_validate(
        response.json()
    )

    assert data.meta.total == len(mock_modules_data)
    assert data.data[0].current_version is not None


def test_get_all_modules_module_owner_f1(test_client, f1_mo_user_login):
    """Test retrieving modules as F1 owner (sees own drafts + all released)."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}
    response = test_client.get("/v0/modules", headers=headers)
    assert response.status_code == 200
    data = PaginatedResponse[model.ModuleResponse].model_validate(
        response.json()
    )

    assert len(data.data) > 0

    own_module = next(m for m in data.data if m.owner_id == "11")
    assert own_module.current_version.status in [
        WorkflowStatus.DRAFT,
        WorkflowStatus.IN_REVIEW,
        WorkflowStatus.VALIDATION_EO,
        WorkflowStatus.APPROVAL_DEANERY,
        WorkflowStatus.IN_REVISION,
        WorkflowStatus.RELEASED,
    ]


def test_get_all_modules_program_coordinator_f1(test_client, f1_pc_user_login):
    """Test retrieving modules as F1 coordinator."""
    headers = {"Authorization": f"Bearer {f1_pc_user_login}"}
    response = test_client.get("/v0/modules", headers=headers)
    assert response.status_code == 200
    data = PaginatedResponse[model.ModuleResponse].model_validate(
        response.json()
    )

    f1_module = next(m for m in data.data if "F1" in m.module_number)
    if f1_module.current_version.status != WorkflowStatus.RELEASED:
        assert f1_module.current_version.status in [
            WorkflowStatus.IN_REVIEW,
            WorkflowStatus.VALIDATION_EO,
            WorkflowStatus.APPROVAL_DEANERY,
        ]


def test_get_all_modules_filter_faculty(test_client, admin_user_login):
    """Test filtering modules by faculty."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/modules?faculty=F1_MECHANICAL_PROCESS_MARITIME", headers=headers
    )
    assert response.status_code == 200
    data = PaginatedResponse[model.ModuleResponse].model_validate(
        response.json()
    )

    for mod in data.data:
        assert mod.module_number.startswith("F1")


def test_get_all_modules_search(test_client, admin_user_login):
    """Test searching modules by title."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    search_term = "Thermodynamics"
    response = test_client.get(
        f"/v0/modules?search={search_term}", headers=headers
    )
    assert response.status_code == 200
    data = PaginatedResponse[model.ModuleResponse].model_validate(
        response.json()
    )

    assert len(data.data) > 0
    assert search_term in data.data[0].title


def test_get_all_modules_sort_title_desc(test_client, admin_user_login):
    """Test sorting modules by title descending."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    response = test_client.get(
        "/v0/modules?sort_by=title&sort_order=desc", headers=headers
    )
    assert response.status_code == 200
    data = PaginatedResponse[model.ModuleResponse].model_validate(
        response.json()
    )

    titles = [module.title for module in data.data]
    assert titles == sorted(titles, reverse=True)


def test_get_modules_unauthenticated(test_client):
    """Test retrieving modules without token."""
    response = test_client.get("/v0/modules")
    assert response.status_code == 401


def test_create_module_success_owner(test_client, f1_mo_user_login):
    """Test creating a module as a Module Owner."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}
    new_module_data = {
        "module_number": "F1-999",
        "title": "New Test Module",
        "ects": 5,
        "valid_from_semester": "WiSe 2025/26",
        "content": "Initial content",
    }
    response = test_client.post(
        "/v0/modules", json=new_module_data, headers=headers
    )
    assert response.status_code == 201
    data = model.ModuleResponse.model_validate(response.json())

    assert data.title == new_module_data["title"]
    assert data.current_version.status == WorkflowStatus.DRAFT
    assert data.owner_id == "11"


def test_create_module_success_admin_set_owner(test_client, admin_user_login):
    """Test creating a module as Admin and setting a specific owner."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    new_module_data = {
        "module_number": "F2-999",
        "title": "Admin Created Module",
        "ects": 6,
        "valid_from_semester": "SoSe 2026",
        "owner_id": "12",
    }
    response = test_client.post(
        "/v0/modules", json=new_module_data, headers=headers
    )
    assert response.status_code == 201
    data = model.ModuleResponse.model_validate(response.json())

    assert data.owner_id == "12"


def test_create_module_forbidden_role(test_client, f1_pc_user_login):
    """Test creating a module as Program Coordinator (should fail)."""
    headers = {"Authorization": f"Bearer {f1_pc_user_login}"}

    new_module_data = {
        "module_number": "F1-888",
        "title": "Forbidden Module",
        "ects": 5,
        "valid_from_semester": "WiSe 2025/26",
    }

    response = test_client.post(
        "/v0/modules", json=new_module_data, headers=headers
    )

    assert response.status_code == 403


def test_get_module_by_id_success(test_client, admin_user_login):
    """Test retrieving a specific module by ID."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    target_module = mock_modules_data[0]
    response = test_client.get(
        f"/v0/modules/{target_module.id}", headers=headers
    )

    assert response.status_code == 200
    data = model.ModuleResponse.model_validate(response.json())
    assert data.id == uuid.UUID(target_module.id)


def test_get_module_by_id_not_found(test_client, admin_user_login):
    """Test retrieving a non-existent module."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}
    random_uuid = uuid.uuid4()
    response = test_client.get(f"/v0/modules/{random_uuid}", headers=headers)
    assert response.status_code == 404


def test_update_version_content_owner_draft(test_client, f1_mo_user_login):
    """Test owner updating their own DRAFT version."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}

    create_resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-UPD-TEST",
            "title": "Update Test",
            "ects": 5,
            "valid_from_semester": "WiSe 25/26",
        },
        headers=headers,
    )
    module_data = model.ModuleResponse.model_validate(create_resp.json())
    version_id = module_data.current_version.id

    update_data = {"content": "Updated content"}
    response = test_client.put(
        f"/v0/modules/versions/{version_id}", json=update_data, headers=headers
    )

    assert response.status_code == 200
    data = model.ModuleVersionResponse.model_validate(response.json())
    assert data.content == "Updated content"


def test_update_version_content_forbidden_status(test_client, admin_user_login):
    """Test updating a RELEASED version (should fail)."""
    headers = {"Authorization": f"Bearer {admin_user_login}"}

    released_version = next(
        v for v in mock_versions_data if v.status == WorkflowStatus.RELEASED
    )

    response = test_client.put(
        f"/v0/modules/versions/{released_version.id}",
        json={"content": "Illegal Update"},
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot edit version in current status."


def test_update_version_content_forbidden_user(test_client, f2_mo_user_login):
    """Test updating a version owned by another user."""
    headers = {"Authorization": f"Bearer {f2_mo_user_login}"}

    target_v_id = None
    for module in mock_modules_data:
        if module.owner_id != "12":
            from utils.development.service import get_uuid_seeded

            target_v_id = get_uuid_seeded(f"{module.module_number}-v4")
            break

    response = test_client.put(
        f"/v0/modules/versions/{target_v_id}",
        json={"content": "Hacked"},
        headers=headers,
    )
    assert response.status_code == 403


def test_workflow_submit_draft(test_client, f1_mo_user_login):
    """Test Owner submitting DRAFT -> IN_REVIEW."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}

    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-WF-1",
            "title": "WF Test",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers,
    )
    version_id = resp.json()["current_version"]["id"]

    status_update = {"status": "IN_REVIEW", "comment": "Ready for review"}
    resp = test_client.patch(
        f"/v0/modules/versions/{version_id}/status",
        json=status_update,
        headers=headers,
    )

    assert resp.status_code == 200
    assert resp.json()["status"] == WorkflowStatus.IN_REVIEW


def test_workflow_pc_approve_content(
    test_client, f1_mo_user_login, f1_pc_user_login
):
    """Test Program Coordinator approving IN_REVIEW -> VALIDATION_EO."""
    headers_mo = {"Authorization": f"Bearer {f1_mo_user_login}"}
    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-WF-2",
            "title": "WF2",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers_mo,
    )
    vid = resp.json()["current_version"]["id"]
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "IN_REVIEW"},
        headers=headers_mo,
    )

    headers_pc = {"Authorization": f"Bearer {f1_pc_user_login}"}
    resp = test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "VALIDATION_EO", "comment": "Looks good"},
        headers=headers_pc,
    )

    assert resp.status_code == 200
    assert resp.json()["status"] == WorkflowStatus.VALIDATION_EO


def test_workflow_pc_reject_content(
    test_client, f1_mo_user_login, f1_pc_user_login
):
    """Test Program Coordinator rejecting IN_REVIEW -> IN_REVISION."""
    headers_mo = {"Authorization": f"Bearer {f1_mo_user_login}"}
    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-WF-3",
            "title": "WF3",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers_mo,
    )
    vid = resp.json()["current_version"]["id"]
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "IN_REVIEW"},
        headers=headers_mo,
    )

    headers_pc = {"Authorization": f"Bearer {f1_pc_user_login}"}
    resp = test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "IN_REVISION", "comment": "Fix this"},
        headers=headers_pc,
    )

    assert resp.status_code == 200
    assert resp.json()["status"] == WorkflowStatus.IN_REVISION


def test_workflow_wrong_faculty_pc(
    test_client, f1_mo_user_login, f2_pc_user_login
):
    """Test F2 Coordinator trying to approve F1 module (should fail)."""
    headers_mo = {"Authorization": f"Bearer {f1_mo_user_login}"}
    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-WF-4",
            "title": "WF4",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers_mo,
    )
    vid = resp.json()["current_version"]["id"]
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "IN_REVIEW"},
        headers=headers_mo,
    )

    headers_pc = {"Authorization": f"Bearer {f2_pc_user_login}"}
    resp = test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "VALIDATION_EO"},
        headers=headers_pc,
    )

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid transition from IN_REVIEW"


def test_workflow_eo_approve(
    test_client, f1_mo_user_login, f1_pc_user_login, eo_user_login
):
    """Test EO approving VALIDATION_EO -> APPROVAL_DEANERY."""
    headers_mo = {"Authorization": f"Bearer {f1_mo_user_login}"}
    headers_pc = {"Authorization": f"Bearer {f1_pc_user_login}"}
    headers_eo = {"Authorization": f"Bearer {eo_user_login}"}

    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-WF-5",
            "title": "WF5",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers_mo,
    )
    vid = resp.json()["current_version"]["id"]
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "IN_REVIEW"},
        headers=headers_mo,
    )
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "VALIDATION_EO"},
        headers=headers_pc,
    )

    resp = test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "APPROVAL_DEANERY"},
        headers=headers_eo,
    )

    assert resp.status_code == 200
    assert resp.json()["status"] == WorkflowStatus.APPROVAL_DEANERY


def test_workflow_deanery_release(
    test_client,
    f1_mo_user_login,
    f1_pc_user_login,
    eo_user_login,
    deanery_user_login,
):
    """Test Deanery approving APPROVAL_DEANERY -> RELEASED."""
    # 1. Setup: ... -> Deanery
    headers_mo = {"Authorization": f"Bearer {f1_mo_user_login}"}
    headers_pc = {"Authorization": f"Bearer {f1_pc_user_login}"}
    headers_eo = {"Authorization": f"Bearer {eo_user_login}"}
    headers_dean = {"Authorization": f"Bearer {deanery_user_login}"}

    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-WF-6",
            "title": "WF6",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers_mo,
    )
    vid = resp.json()["current_version"]["id"]
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "IN_REVIEW"},
        headers=headers_mo,
    )
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "VALIDATION_EO"},
        headers=headers_pc,
    )
    test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "APPROVAL_DEANERY"},
        headers=headers_eo,
    )
    resp = test_client.patch(
        f"/v0/modules/versions/{vid}/status",
        json={"status": "RELEASED"},
        headers=headers_dean,
    )

    assert resp.status_code == 200
    assert resp.json()["status"] == WorkflowStatus.RELEASED


def test_add_translation_owner(test_client, f1_mo_user_login):
    """Test Owner adding a translation."""
    headers = {"Authorization": f"Bearer {f1_mo_user_login}"}
    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-TR-1",
            "title": "Trans Test",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers,
    )
    vid = resp.json()["current_version"]["id"]

    trans_data = {
        "language": "de",
        "title": "Übersetzter Titel",
        "content": "Inhalt auf Deutsch",
    }

    resp = test_client.post(
        f"/v0/modules/versions/{vid}/translations",
        json=trans_data,
        headers=headers,
    )

    assert resp.status_code == 201
    data = model.TranslationResponse.model_validate(resp.json())
    assert data.title == trans_data["title"]
    assert data.language == "de"


def test_add_translation_forbidden(
    test_client, f2_mo_user_login, f1_mo_user_login
):
    """Test non-owner adding a translation (fail)."""
    headers_f1 = {"Authorization": f"Bearer {f1_mo_user_login}"}
    resp = test_client.post(
        "/v0/modules",
        json={
            "module_number": "F1-TR-2",
            "title": "T2",
            "ects": 5,
            "valid_from_semester": "W",
        },
        headers=headers_f1,
    )
    vid = resp.json()["current_version"]["id"]

    headers_f2 = {"Authorization": f"Bearer {f2_mo_user_login}"}
    trans_data = {"language": "de", "title": "Hack", "content": "Hack"}
    resp = test_client.post(
        f"/v0/modules/versions/{vid}/translations",
        json=trans_data,
        headers=headers_f2,
    )
    assert resp.status_code == 403
