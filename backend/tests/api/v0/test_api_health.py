"""Tests for the API health endpoints.

This module contains tests to verify the health status of the server
using the /v0/health/running and /v0/health/ready endpoints.
"""
from api.v0.routes.health.model import ReadyResponse
from api.v0.routes.health.model import RunningResponse


def test_server_running(test_client):
    """Test the /v0/health/running endpoint."""
    response = test_client.get("/v0/health/running")
    assert response.status_code == 200
    data = RunningResponse.model_validate(response.json())
    assert data.status == "pass"


def test_server_ready(test_client):
    """Test the /v0/health/ready endpoint."""
    response = test_client.get("/v0/health/ready")
    assert response.status_code == 200
    data = ReadyResponse.model_validate(response.json())
    assert data.status == "pass"
    assert data.details.database == "pass"
