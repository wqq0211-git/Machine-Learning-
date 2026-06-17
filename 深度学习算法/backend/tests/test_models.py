from fastapi.testclient import TestClient

from main import app


def test_models_returns_two_models():
    response = TestClient(app).get("/api/models")
    assert response.status_code == 200
    data = response.json()["data"]
    assert {item["id"] for item in data} == {"cnn", "resnet18"}


def test_dataset_format():
    response = TestClient(app).get("/api/dataset")
    assert response.status_code == 200
    assert len(response.json()["data"]["classes"]) == 10

