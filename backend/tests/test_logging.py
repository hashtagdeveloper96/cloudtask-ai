from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_request_id_header():
    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200

    assert "x-request-id" in response.headers

    assert response.headers[
        "x-request-id"
    ]
