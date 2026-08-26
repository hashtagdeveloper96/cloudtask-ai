from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "CloudTask AI Development API"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "development"


def test_readiness_check():
    response = client.get("/api/v1/ready")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ready"
    assert data["service"] == "CloudTask AI Development API"

