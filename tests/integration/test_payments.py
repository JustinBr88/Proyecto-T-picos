import pytest

from tests.support import CARD_NUMBER, CUSTOMER, future

pytestmark = pytest.mark.integration
USERNAME = CUSTOMER["username"]


def test_list_cards(client):
    response = client.get("/api/payment", query_string={"username": USERNAME})
    assert response.status_code == 200
    assert [card["card_number"] for card in response.get_json()] == [CARD_NUMBER]


def test_add_and_delete_card(client):
    response = client.post("/api/payment", json={
        "username": USERNAME, "card_number": "5555555555554444", "name": "Test User", "cvv": "321",
        "expiration_date": future(400)})
    assert response.status_code == 200

    response = client.delete("/api/payment", query_string={"username": USERNAME, "card_number": "5555555555554444"})
    assert response.status_code == 200

    cards = client.get("/api/payment", query_string={"username": USERNAME}).get_json()
    assert [card["card_number"] for card in cards] == [CARD_NUMBER]


def test_cannot_delete_card_used_in_future_reservation(client, make_reservation):
    make_reservation(check_in_days=10)
    response = client.delete("/api/payment", query_string={"username": USERNAME, "card_number": CARD_NUMBER})
    assert response.status_code == 400


def test_reservations_by_card_number(client, make_reservation):
    reservation_id = make_reservation()
    response = client.get("/api/reservation/cardNumber", query_string={"username": USERNAME,
                                                                       "card_number": CARD_NUMBER})
    assert [r["reservation_id"] for r in response.get_json()] == [reservation_id]
