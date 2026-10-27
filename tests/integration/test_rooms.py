"""Búsqueda de habitaciones y disponibilidad por mes (Caso 2)."""
from datetime import date

import pytest

from tests.support import CARD_NUMBER, CUSTOMER, LOCATION, ROOMS, future

pytestmark = pytest.mark.integration
USERNAME = CUSTOMER["username"]


def _search(client, check_in_days, check_out_days):
    response = client.get("/api/searchRoom", query_string={
        "location": LOCATION, "checkIn": future(check_in_days), "checkOut": future(check_out_days)})
    assert response.status_code == 200
    return sorted(room["room_number"] for room in response.get_json()["response"])


@pytest.mark.parametrize("search", [(12, 20), (5, 12), (11, 13), (5, 20)],
                         ids=["empieza-dentro", "termina-dentro", "contenida", "envuelve"])
def test_search_hides_rooms_with_overlapping_reservations(client, make_reservation, search):
    """Regresión BUG-1 (CA2.1): reserva del día 10 al 15, búsquedas que se solapan."""
    make_reservation(check_in_days=10, nights=5, room=ROOMS[0])
    assert _search(client, *search) == [102]


def test_search_offers_room_when_checkin_is_previous_checkout(client, make_reservation):
    """CA2.2: check-in el día del check-out de otra reserva."""
    make_reservation(check_in_days=10, nights=5, room=ROOMS[0])
    assert _search(client, 15, 18) == [101, 102]


def test_create_reservation_rejects_a_room_already_booked(client, make_reservation):
    """Sin esta validación, una pantalla desactualizada o una llamada directa a la API reservaba dos veces."""
    make_reservation(check_in_days=10, nights=5, room=ROOMS[0])
    location, number, _, cost, _, extra_bed_price = ROOMS[0]
    response = client.post("/api/reservation/create", json={
        "username": USERNAME, "checkIn": future(12), "checkOut": future(14), "card_number": CARD_NUMBER,
        "rooms": [{"location": location, "room_number": number, "cost": cost,
                   "extra_bed_price": extra_bed_price, "extra_bed_or_not": 0}]})
    assert response.status_code == 400
    assert response.get_json()["result"] is False


def test_update_rejects_dates_that_overlap_another_reservation(client, make_reservation):
    """Regresión BUG-1 en is_room_free: mover una reserva encima de otra."""
    make_reservation(check_in_days=10, nights=5, room=ROOMS[0])
    other = make_reservation(check_in_days=30, nights=2, room=ROOMS[0])
    response = client.put("/api/reservation", json={
        "username": USERNAME, "reservation_id": str(other), "checkIn": future(13), "checkOut": future(16)})
    assert response.status_code == 400


def _availability(client, day_offset, location=LOCATION):
    month = future(day_offset)[:7]
    response = client.get("/api/availability", query_string={"location": location, "month": month})
    return response


def _status(client, day_offset):
    response = _availability(client, day_offset)
    assert response.status_code == 200, response.get_json()
    days = {day["date"]: day for day in response.get_json()["days"]}
    return days[future(day_offset)]


def test_availability_returns_every_day_of_the_month(client):
    response = _availability(client, 10)
    body = response.get_json()
    year, month = (int(part) for part in future(10)[:7].split("-"))
    first = date(year, month, 1)
    assert response.status_code == 200
    assert (body["result"], body["location"], body["month"]) == (True, LOCATION, future(10)[:7])
    assert body["days"][0]["date"] == first.isoformat()
    assert {day["status"] for day in body["days"]} == {"libre"}
    assert body["days"][0]["total_rooms"] == len(ROOMS)


def test_availability_marks_partial_and_full_days(client, make_reservation):
    """CA2.4: un día con una de dos habitaciones ocupadas es parcial; con las dos, lleno."""
    make_reservation(check_in_days=10, nights=2, room=ROOMS[0])
    make_reservation(check_in_days=11, nights=1, room=ROOMS[1])
    assert _status(client, 10)["status"] == "parcial"
    assert _status(client, 11)["status"] == "lleno"
    assert _status(client, 11)["free_rooms"] == 0
    assert _status(client, 12)["status"] == "libre"   # día de check-out de ambas


def test_cancelled_reservations_do_not_occupy_days(client, make_reservation):
    """CA2.3."""
    reservation_id = make_reservation(check_in_days=10, nights=2, room=ROOMS[0])
    client.get(f"/api/reservation/{reservation_id}/cancel", query_string={"username": USERNAME})
    assert _status(client, 10)["status"] == "libre"


@pytest.mark.parametrize("month", ["2026-13", "noviembre", "2026-1"])
def test_availability_rejects_invalid_month(client, month):
    response = client.get("/api/availability", query_string={"location": LOCATION, "month": month})
    assert response.status_code == 400


def test_availability_requires_location_and_month(client):
    assert client.get("/api/availability", query_string={"location": LOCATION}).status_code == 400
    assert client.get("/api/availability", query_string={"month": "2026-11"}).status_code == 400


def test_availability_of_unknown_location_is_404(client):
    response = _availability(client, 10, location="Narnia")
    assert response.status_code == 404
    assert response.get_json()["result"] is False
