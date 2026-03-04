from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)


@pytest.mark.integration
def test_admin_route_not_available():
    response = client.get("/admin/projects")
    assert response.status_code == 404


@pytest.mark.integration
def test_public_route_available():
    response = client.get("/projects")
    assert response.status_code == 200
