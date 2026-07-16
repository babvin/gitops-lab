from fastapi.testclient import TestClient


def test_healthz_returns_200(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200


def test_healthz_payload_shape(client: TestClient) -> None:
    response = client.get("/healthz")
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "sample-api"
    assert "version" in body
