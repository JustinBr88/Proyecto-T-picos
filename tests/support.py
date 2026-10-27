"""Datos y utilidades compartidos por los tests."""
from datetime import date, timedelta

CUSTOMER = {"username": "Ctest", "password": "secret12", "first_name": "Test", "last_name": "User",
            "email": "ctest@fancyhotel.test"}
MANAGER = {"username": "Mtest", "password": "admin12"}
CARD_NUMBER = "4111111111111111"
LOCATION = "Atlanta"
ROOMS = [
    # location, room_number, type, room_cost, capacity, extra_bed_price
    (LOCATION, 101, "Standard", 100.0, 2, 10.0),
    (LOCATION, 102, "Suite", 200.0, 4, 30.0),
]


def future(days):
    """Fecha ISO relativa a hoy, para que los tests no caduquen."""
    return (date.today() + timedelta(days=days)).isoformat()
