from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_task():
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "status": "pending",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["status"] == "pending"
    assert "id" in data


def test_get_tasks():
    response = client.get("/api/v1/tasks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_missing_task():
    response = client.get("/api/v1/tasks/999999")

    assert response.status_code == 404
