from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    # Create a unique user for the test
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "tasktest@example.com",
            "username": "tasktestuser",
            "password": "TestPassword123!",
        },
    )

    # If the user already exists, that's okay.
    assert register_response.status_code in (201, 409)

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "tasktest@example.com",
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_task():
    headers = get_auth_headers()

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "status": "pending",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["description"] == "Testing task creation"
    assert data["status"] == "pending"


def test_get_tasks():
    headers = get_auth_headers()

    response = client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_missing_task():
    headers = get_auth_headers()

    response = client.get(
        "/api/v1/tasks/999999",
        headers=headers,
    )

    assert response.status_code == 404
