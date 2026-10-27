import pytest

from tests.support import CARD_NUMBER, CUSTOMER, LOCATION, ROOMS, future

pytestmark = pytest.mark.integration
USERNAME = CUSTOMER["username"]


def _get(client, reservation_id):
    return client.get(f"/api/reservation/{reservation_id}", query_string={"username": USERNAME})


def test_create_reservation_computes_total_cost(client, make_reservation):
    reservation_id = make_reservation(nights=3, room=ROOMS[0], extra_bed=1)
    data = _get(client, reservation_id).get_json()["data"]
    assert data["total_cost"] == (100.0 + 10.0) * 3
    assert data["card_number"] == CARD_NUMBER
    assert data["rooms"][0]["room_number"] == 101


def test_create_reservation_requires_rooms(client):
    response = client.post("/api/reservation/create", json={
        "username": USERNAME, "checkIn": future(1), "checkOut": future(2), "card_number": CARD_NUMBER,
        "rooms": []})
    assert response.status_code == 400


def test_get_reservation_of_another_user_returns_404(client, make_reservation):
    reservation_id = make_reservation()
    response = client.get(f"/api/reservation/{reservation_id}", query_string={"username": "Cxxxx"})
    assert response.status_code == 404


def test_reserved_room_is_not_offered_for_the_same_dates(client, make_reservation):
    make_reservation(check_in_days=10, nights=2, room=ROOMS[0])
    response = client.get("/api/searchRoom", query_string={
        "location": LOCATION, "checkIn": future(10), "checkOut": future(12)})
    assert [room["room_number"] for room in response.get_json()["response"]] == [102]


def test_update_reservation_dates_via_frontend_endpoint(client, make_reservation):
    """Regresión BUG-2: PUT /api/reservation/<id> (el que usa el frontend) fallaba con NameError."""
    reservation_id = make_reservation(check_in_days=10, nights=2)
    response = client.put(f"/api/reservation/{reservation_id}", json={
        "username": USERNAME, "checkIn": future(20), "checkOut": future(24)})
    assert response.status_code == 200, response.get_json()

    data = _get(client, reservation_id).get_json()["data"]
    assert data["checkin_date"] == future(20)
    assert data["total_cost"] == 100.0 * 4


def test_availability_check_for_new_dates(client, make_reservation):
    reservation_id = make_reservation()
    response = client.get(f"/api/reservation/{reservation_id}/availability", query_string={
        "username": USERNAME, "checkIn": future(30), "checkOut": future(32)})
    assert response.status_code == 200
    assert response.get_json()["result"] is True


def test_cancel_reservation_well_in_advance_costs_nothing(client, make_reservation):
    reservation_id = make_reservation(check_in_days=10)
    response = client.get(f"/api/reservation/{reservation_id}/cancel", query_string={"username": USERNAME})
    assert response.status_code == 200

    # Una reserva cancelada ya no se puede consultar ni volver a cancelar.
    assert _get(client, reservation_id).status_code == 404
    response = client.get(f"/api/reservation/{reservation_id}/cancel", query_string={"username": USERNAME})
    assert response.status_code == 400


def test_cancelled_reservation_frees_the_room(client, make_reservation):
    reservation_id = make_reservation(check_in_days=10, nights=2, room=ROOMS[0])
    client.get(f"/api/reservation/{reservation_id}/cancel", query_string={"username": USERNAME})
    response = client.get("/api/searchRoom", query_string={
        "location": LOCATION, "checkIn": future(10), "checkOut": future(12)})
    assert {room["room_number"] for room in response.get_json()["response"]} == {101, 102}
