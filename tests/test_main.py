from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_app_loads():
    response = client.get("/")
    assert response.status_code in [404, 200]


def test_validation_exception():
    response = client.get("/provider/digitain/odds", params={"match_id": "fake"})
    assert response.status_code == 400
    assert "detail" in response.json()
