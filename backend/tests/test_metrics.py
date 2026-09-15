from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200

    assert "cloudtask_http_requests_total" in response.text

    assert "cloudtask_http_request_duration_seconds" in response.text
