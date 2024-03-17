from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_users():
    response = client.get("/user")
    assert response.status_code == 200


def test_get_all_staffs():
    response = client.get("/staffs")
    assert response.status_code == 200


def test_get_all_services():
    response = client.get("/service")
    assert response.status_code == 200
