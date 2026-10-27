"""Reglas de disponibilidad del Caso 2: lógica pura, sin base de datos."""
from datetime import date

import pytest

from fancyhotel.availability import FREE, FULL, PARTIAL, day_status, monthly_availability, overlaps, parse_month

# Reserva existente del 10 al 15 (ocupa las noches 10, 11, 12, 13 y 14).
STAY = (date(2026, 11, 10), date(2026, 11, 15))


@pytest.mark.parametrize("query", [
    (date(2026, 11, 12), date(2026, 11, 20)),  # empieza dentro, termina después (caso del CA2.1)
    (date(2026, 11, 5), date(2026, 11, 12)),   # empieza antes, termina dentro
    (date(2026, 11, 11), date(2026, 11, 13)),  # contenida en la reserva
    (date(2026, 11, 5), date(2026, 11, 20)),   # envuelve a la reserva
    (date(2026, 11, 10), date(2026, 11, 15)),  # mismas fechas
])
def test_overlapping_stays_are_detected(query):
    """Regresión BUG-1: el original sólo detectaba reservas contenidas en la búsqueda."""
    assert overlaps(*STAY, *query)


@pytest.mark.parametrize("query", [
    (date(2026, 11, 15), date(2026, 11, 18)),  # check-in el día del check-out (CA2.2)
    (date(2026, 11, 7), date(2026, 11, 10)),   # check-out el día del check-in (CA2.2)
    (date(2026, 11, 20), date(2026, 11, 22)),  # totalmente después
])
def test_non_overlapping_stays_are_free(query):
    assert not overlaps(*STAY, *query)


def test_overlaps_also_works_with_iso_strings():
    assert overlaps("2026-11-10", "2026-11-15", "2026-11-12", "2026-11-20")
    assert not overlaps("2026-11-10", "2026-11-15", "2026-11-15", "2026-11-18")


def _status_by_day(days):
    return {day["date"]: day["status"] for day in days}


def test_month_without_reservations_is_all_free():
    days = monthly_availability(2027, 2, total_rooms=2, stays=[])
    assert len(days) == 28
    assert {day["status"] for day in days} == {FREE}
    assert days[0] == {"date": "2027-02-01", "status": FREE, "free_rooms": 2, "total_rooms": 2}


@pytest.mark.parametrize("free_rooms, expected", [
    (10, FREE),
    (4, FREE),      # 40 % libre: todavía hay de sobra
    (3, PARTIAL),   # 30 % libre: el límite cuenta como "pocas"
    (1, PARTIAL),
    (0, FULL),
])
def test_partial_means_thirty_percent_or_less_free(free_rooms, expected):
    """CA2.4: "parcial" avisa que quedan pocas, no que hay alguna ocupada (decisión humana #8)."""
    assert day_status(free_rooms, total_rooms=10) == expected


@pytest.mark.parametrize("total_rooms, free_rooms", [(20, 6), (30, 9), (70, 21)])
def test_exact_thirty_percent_boundary_is_partial_for_any_size(total_rooms, free_rooms):
    assert day_status(free_rooms, total_rooms) == PARTIAL
    assert day_status(free_rooms + 1, total_rooms) == FREE


def test_half_booked_hotel_is_still_free():
    assert day_status(1, total_rooms=2) == FREE


def test_full_day_and_checkout_night_with_two_rooms():
    stays = [
        ("Atlanta", 101, date(2026, 11, 10), date(2026, 11, 13)),
        ("Atlanta", 102, date(2026, 11, 12), date(2026, 11, 14)),
    ]
    status = _status_by_day(monthly_availability(2026, 11, total_rooms=2, stays=stays))
    assert status["2026-11-09"] == FREE
    assert status["2026-11-12"] == FULL
    assert status["2026-11-13"] == FREE      # el 101 hace check-out: esa noche queda libre (CA2.2)


def test_monthly_availability_marks_partial_days():
    stays = [("Atlanta", room, date(2026, 11, 10), date(2026, 11, 12)) for room in range(101, 108)]
    day = next(d for d in monthly_availability(2026, 11, total_rooms=10, stays=stays) if d["date"] == "2026-11-10")
    assert (day["free_rooms"], day["status"]) == (3, PARTIAL)


def test_stay_crossing_month_boundaries_only_counts_nights_inside_the_month():
    stays = [("Atlanta", 101, date(2026, 10, 30), date(2026, 11, 2))]
    status = _status_by_day(monthly_availability(2026, 11, total_rooms=1, stays=stays))
    assert status["2026-11-01"] == FULL
    assert status["2026-11-02"] == FREE


def test_a_double_booked_room_is_counted_once():
    """Con BUG-1 pudieron quedar reservas solapadas en la misma habitación: no puede dar libres negativos."""
    stays = [
        ("Atlanta", 101, date(2026, 11, 10), date(2026, 11, 15)),
        ("Atlanta", 101, date(2026, 11, 12), date(2026, 11, 20)),
    ]
    day = next(d for d in monthly_availability(2026, 11, total_rooms=2, stays=stays) if d["date"] == "2026-11-12")
    assert day["free_rooms"] == 1


def test_parse_month_accepts_year_and_month():
    assert parse_month("2026-11") == (2026, 11)


@pytest.mark.parametrize("text", ["2026-13", "2026-1", "26-11", "noviembre", "2026-11-01", ""])
def test_parse_month_rejects_invalid_values(text):
    with pytest.raises(ValueError):
        parse_month(text)
