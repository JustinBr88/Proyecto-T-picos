"""Fixtures compartidas.

- Los tests unitarios (tests/unit) no necesitan base de datos.
- Los de integración (tests/integration) usan la base TEST_DB_NAME, que se
  borra y se recrea antes de CADA test con un juego de datos mínimo y conocido.
  Si MySQL no está corriendo, se marcan como "skipped" con el motivo.
"""
import mysql.connector
import pytest

from fancyhotel import create_app
from fancyhotel.config import Config
from fancyhotel.db import schema
from fancyhotel.db.connection import get_db
from tests.support import CARD_NUMBER, CUSTOMER, MANAGER, ROOMS, future


@pytest.fixture(scope="session")
def app():
    if Config.TEST_DB_NAME == Config.DB_NAME:
        pytest.exit("TEST_DB_NAME no puede ser igual a DB_NAME: los tests borran la base.")

    app = create_app({"TESTING": True, "DB_NAME": Config.TEST_DB_NAME})
    try:
        with app.app_context():
            schema.create_database()
    except mysql.connector.Error as error:
        pytest.skip(f"MySQL no disponible ({error}). Levantalo con: docker compose up -d")
    return app


def _insert_fixture_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Manager (username, password) VALUES (%(username)s, %(password)s)", MANAGER)
    cursor.execute(
        """INSERT INTO Customer (username, password, first_name, last_name, email)
        VALUES (%(username)s, %(password)s, %(first_name)s, %(last_name)s, %(email)s)""",
        CUSTOMER)
    cursor.execute(
        """INSERT INTO Credit_Card (card_number, name, cvv, expiration_date, username)
        VALUES (%s, %s, %s, %s, %s)""",
        (CARD_NUMBER, "Test User", "123", future(3 * 365), CUSTOMER["username"]))
    cursor.executemany(
        """INSERT INTO Room (location, room_number, type, room_cost, capacity, extra_bed_price)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        ROOMS)
    db.commit()
    cursor.close()


@pytest.fixture
def db(app):
    with app.app_context():
        schema.init_schema(reset=True)
        _insert_fixture_data()
    yield


@pytest.fixture
def client(app, db):
    return app.test_client()


@pytest.fixture
def make_reservation(client):
    """Crea una reserva por la API y devuelve su id."""
    def _make(check_in_days=10, nights=2, room=ROOMS[0], extra_bed=0):
        location, number, _, cost, _, extra_bed_price = room
        response = client.post("/api/reservation/create", json={
            "username": CUSTOMER["username"],
            "checkIn": future(check_in_days),
            "checkOut": future(check_in_days + nights),
            "card_number": CARD_NUMBER,
            "rooms": [{"location": location, "room_number": number, "cost": cost,
                       "extra_bed_price": extra_bed_price, "extra_bed_or_not": extra_bed}],
        })
        assert response.status_code == 200, response.get_json()
        return response.get_json()["id"]
    return _make
