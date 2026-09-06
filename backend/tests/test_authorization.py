from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_user_and_login():
    unique_id = uuid4().hex[:8]

    email = f"user_{unique_id}@example.com"
    username = f"user_{unique_id}"
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

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_tasks_require_authentication():
    response = client.get("/api/v1/tasks")

    assert response.status_code in (401, 403)


def test_authenticated_user_can_create_task():
    headers = create_user_and_login()

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Authorization Test Task",
            "description": "Testing authenticated task creation",
            "status": "pending",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Authorization Test Task"
    assert data["status"] == "pending"
    assert "user_id" in data


def test_user_cannot_access_another_users_task():
    user_a_headers = create_user_and_login()
    user_b_headers = create_user_and_login()

    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "User A Private Task",
            "description": "User B must not access this task",
            "status": "pending",
        },
        headers=user_a_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=user_b_headers,
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_task():
    user_a_headers = create_user_and_login()
    user_b_headers = create_user_and_login()

    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Private Task",
            "description": "Only User A can update",
            "status": "pending",
        },
        headers=user_a_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "status": "completed",
        },
        headers=user_b_headers,
    )

    assert update_response.status_code == 404


def test_user_cannot_delete_another_users_task():
    user_a_headers = create_user_and_login()
    user_b_headers = create_user_and_login()

    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Do Not Delete",
            "description": "Owned by User A",
            "status": "pending",
        },
        headers=user_a_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=user_b_headers,
    )

    assert delete_response.status_code == 404

    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=user_a_headers,
    )

    assert get_response.status_code == 200


def test_user_can_update_own_task():
    headers = create_user_and_login()

    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn Docker",
            "description": "CloudTask AI Docker work",
            "status": "pending",
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "status": "completed",
        },
        headers=headers,
    )

    assert update_response.status_code == 200

    assert update_response.json()["status"] == "completed"


def test_user_can_delete_own_task():
    headers = create_user_and_login()

    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Temporary Task",
            "description": "This task will be deleted",
            "status": "pending",
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert get_response.status_code == 404
