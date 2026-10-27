"""El generador de datos de prueba debe producir datos coherentes."""
import random
from collections import defaultdict
from datetime import date

from fancyhotel.db import seed

TODAY = date(2026, 10, 27)


def _generate(history_months=15):
    rooms = seed.build_rooms()
    customers = seed.build_customers()
    _, card_by_user = seed.build_cards(customers, TODAY)
    start = seed._add_months(TODAY, -history_months)
    end = date(2026, 12, 26)
    return seed.build_reservations(random.Random(seed.RANDOM_SEED), rooms, customers, card_by_user, start, end)


def test_rooms_cover_all_frontend_locations_and_types():
    rooms = seed.build_rooms()
    assert {room[0] for room in rooms} == set(seed.LOCATIONS)
    assert {room[2] for room in rooms} == {"Standard", "Family", "Suite"}
    assert len({(room[0], room[1]) for room in rooms}) == len(rooms), "habitaciones duplicadas"


def test_usernames_fit_schema_and_login_rules():
    for username, password, *_ in seed.build_customers():
        assert len(username) == 5 and username.startswith("C")
        assert len(password) <= 16
    assert seed.MANAGER[0].startswith("M") and len(seed.MANAGER[0]) == 5


def test_reservations_never_overlap_in_the_same_room():
    reservations, reserved_rooms = _generate()
    dates = {r[0]: (r[1], r[2]) for r in reservations}
    stays_by_room = defaultdict(list)
    for location, number, reservation_id, _ in reserved_rooms:
        stays_by_room[(location, number)].append(dates[reservation_id])

    for stays in stays_by_room.values():
        stays.sort()
        for (_, previous_checkout), (next_checkin, _) in zip(stays, stays[1:]):
            assert next_checkin >= previous_checkout


def test_history_spans_requested_months_and_includes_future_bookings():
    reservations, _ = _generate(history_months=15)
    checkins = [r[1] for r in reservations]
    assert min(checkins) < date(2025, 8, 1)
    assert max(checkins) > TODAY


def test_summer_has_more_demand_than_winter():
    """La estacionalidad es lo que permite probar la previsión del Caso 3."""
    reservations, _ = _generate()
    active = [r for r in reservations if r[6] == "0"]
    july = sum(1 for r in active if r[1].month == 7)
    february = sum(1 for r in active if r[1].month == 2)
    assert july > february


def test_generation_is_deterministic():
    assert _generate() == _generate()
