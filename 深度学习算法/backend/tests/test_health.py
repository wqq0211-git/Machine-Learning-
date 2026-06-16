from fastapi.testclient import TestClient

from main import app


def test_health_returns_success():
    response = TestClient(app).get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"]["status"] == "running"

