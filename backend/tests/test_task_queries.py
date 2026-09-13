from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def auth_headers():
    unique = uuid4().hex[:8]

    email = f"query_{unique}@example.com"
    username = f"query_{unique}"
    password = "TestPassword123!"

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()[
        "access_token"
    ]

    return {
        "Authorization": f"Bearer {token}"
    }
  
def test_task_pagination():
    headers = auth_headers()

    for i in range(5):
        response = client.post(
            "/api/v1/tasks",
            json={
                "title": f"Task {i}",
                "status": "pending",
            },
            headers=headers,
        )

        assert response.status_code == 201

    response = client.get(
        "/api/v1/tasks?skip=0&limit=2",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 2
def test_task_status_filter():
    headers = auth_headers()

    client.post(
        "/api/v1/tasks",
        json={
            "title": "Pending Task",
            "status": "pending",
        },
        headers=headers,
    )

    client.post(
        "/api/v1/tasks",
        json={
            "title": "Completed Task",
            "status": "completed",
        },
        headers=headers,
    )

    response = client.get(
        "/api/v1/tasks?status=completed",
        headers=headers,
    )

    assert response.status_code == 200

    tasks = response.json()

    assert all(
        task["status"] == "completed"
        for task in tasks
    )
def test_invalid_task_status():
    headers = auth_headers()

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Invalid Task",
            "status": "wrong_status",
        },
        headers=headers,
    )

    assert response.status_code == 422
