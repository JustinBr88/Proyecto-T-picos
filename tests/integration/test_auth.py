import pytest

from tests.support import CUSTOMER, MANAGER

pytestmark = pytest.mark.integration


def test_register_then_login(client):
    response = client.post("/api/register", json={
        "username": "Cnew1", "email": "new@fancyhotel.test", "password": "pw123456",
        "firstName": "New", "lastName": "User"})
    assert response.status_code == 200
    assert response.get_json()["result"] is True

    response = client.post("/api/login", json={"username": "Cnew1", "password": "pw123456"})
    assert response.status_code == 200


def test_register_rejects_existing_username(client):
    response = client.post("/api/register", json={
        "username": CUSTOMER["username"], "email": "other@fancyhotel.test", "password": "x",
        "firstName": "A", "lastName": "B"})
    assert response.status_code == 400


def test_register_rejects_existing_email(client):
    response = client.post("/api/register", json={
        "username": "Cnew2", "email": CUSTOMER["email"], "password": "x", "firstName": "A", "lastName": "B"})
    assert response.status_code == 400


def test_customer_and_manager_can_login(client):
    for user in (CUSTOMER, MANAGER):
        response = client.post("/api/login", json={"username": user["username"], "password": user["password"]})
        assert response.status_code == 200, user["username"]


def test_login_rejects_wrong_password(client):
    response = client.post("/api/login", json={"username": CUSTOMER["username"], "password": "wrong"})
    assert response.status_code == 401


def test_login_rejects_unknown_role_prefix(client):
    response = client.post("/api/login", json={"username": "Xuser", "password": "x"})
    assert response.status_code == 401
