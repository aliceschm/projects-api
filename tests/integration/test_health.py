from fastapi.testclient import TestClient
import pytest
from src.main import app

client = TestClient(app)

@pytest.mark.integration
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
