"""La app levanta y los endpoints básicos responden."""
import pytest

from tests.support import LOCATION, future

pytestmark = pytest.mark.integration


def test_index_serves_frontend(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"FancyHotelApp" in response.data


def test_search_rooms_get_with_query_string(client):
    """Regresión: con Flask 3 los GET de flask-restful devolvían 415."""
    response = client.get("/api/searchRoom", query_string={
        "location": LOCATION, "checkIn": future(5), "checkOut": future(7)})
    assert response.status_code == 200
    body = response.get_json()
    assert body["result"] is True
    assert {room["room_number"] for room in body["response"]} == {101, 102}


def test_search_rooms_requires_parameters(client):
    response = client.get("/api/searchRoom", query_string={"location": LOCATION})
    assert response.status_code == 400
