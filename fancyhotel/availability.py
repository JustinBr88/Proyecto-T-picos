"""Reglas de disponibilidad (Caso 2): lógica pura, sin base de datos ni HTTP.

Una estadía ocupa las noches desde el check-in hasta el día anterior al
check-out: el rango es [check-in, check-out). Por eso un huésped puede hacer
check-in el mismo día que otro hace check-out.
"""
import calendar
import re
from datetime import date, timedelta

FREE = "libre"
PARTIAL = "parcial"
FULL = "lleno"

# Un día es "parcial" cuando queda esta fracción de habitaciones libres o menos.
# Decisión humana #8 (AI_LOG): con "cualquier habitación ocupada" casi todos los
# días salían parciales y la marca no le decía nada al cliente.
PARTIAL_THRESHOLD_PERCENT = 30

_MONTH_PATTERN = re.compile(r"^(\d{4})-(\d{2})$")


def overlaps(stay_checkin, stay_checkout, query_checkin, query_checkout):
    """True si dos estadías comparten al menos una noche.

    Acepta fechas (`date`) o textos ISO `YYYY-MM-DD`, que se comparan bien
    como texto. Es la misma condición que usa el SQL de db/rooms.py.
    """
    return stay_checkin < query_checkout and stay_checkout > query_checkin


def parse_month(text):
    """Convierte `YYYY-MM` en (año, mes). Lanza ValueError si el formato no es válido."""
    match = _MONTH_PATTERN.match(text or "")
    if not match:
        raise ValueError("El mes debe tener el formato YYYY-MM")
    year, month = int(match.group(1)), int(match.group(2))
    if not 1 <= month <= 12:
        raise ValueError("El mes debe estar entre 01 y 12")
    return year, month


def month_range(year, month):
    """Primer día del mes y primer día del mes siguiente: el rango [inicio, fin)."""
    first = date(year, month, 1)
    return first, first + timedelta(days=calendar.monthrange(year, month)[1])


def day_status(free_rooms, total_rooms):
    """lleno: ninguna libre · parcial: 30 % o menos libres · libre: el resto."""
    if free_rooms <= 0:
        return FULL
    if free_rooms * 100 <= total_rooms * PARTIAL_THRESHOLD_PERCENT:
        return PARTIAL
    return FREE


def monthly_availability(year, month, total_rooms, stays):
    """Estado de cada día del mes.

    `stays` son las reservas activas como tuplas (locación, habitación,
    check-in, check-out). Una habitación con dos reservas solapadas (posible
    con datos viejos, por BUG-1) se cuenta una sola vez.
    """
    first, end = month_range(year, month)
    days = []
    current = first
    while current < end:
        next_day = current + timedelta(days=1)
        occupied = {(location, room) for location, room, checkin, checkout in stays
                    if overlaps(checkin, checkout, current, next_day)}
        free_rooms = max(total_rooms - len(occupied), 0)
        days.append({
            "date": current.isoformat(),
            "status": day_status(free_rooms, total_rooms),
            "free_rooms": free_rooms,
            "total_rooms": total_rooms,
        })
        current = next_day
    return days
