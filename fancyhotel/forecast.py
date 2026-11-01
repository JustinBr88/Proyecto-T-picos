"""Monthly stay demand. Checkout is exclusive; current inventory is used as capacity."""
from collections import defaultdict
from datetime import date, timedelta
from calendar import monthrange


def next_month(day):
    return date(day.year + (day.month == 12), day.month % 12 + 1, 1)


def monthly_series(stays, capacities, start, end):
    """Count distinct room nights even if conflicting reservations overlap."""
    nights = defaultdict(set)
    reservations = defaultdict(set)
    rooms = defaultdict(set)
    for reservation_id, checkin, checkout, location, room_number in stays:
        if checkout <= checkin:
            continue
        day = max(checkin, start)
        while day < min(checkout, end):
            month = day.replace(day=1)
            nights[(month, location)].add((day, room_number))
            reservations[(month, location)].add(reservation_id)
            rooms[(month, location)].add(room_number)
            day += timedelta(days=1)
    output = []
    month = start
    while month < end:
        for location, capacity in capacities.items():
            key = (month, location)
            occupied = len(nights[key])
            available = capacity * monthrange(month.year, month.month)[1]
            output.append({"month": month.isoformat()[:7], "location": location,
                           "reservations": len(reservations[key]), "rooms": len(rooms[key]),
                           "room_nights": occupied, "capacity_room_nights": available,
                           "occupancy_percent": round(100 * occupied / available, 1) if available else None})
        month = next_month(month)
    return output


def moving_average(values, horizon):
    """Recursive three-month moving average; rounded only for display."""
    if len(values) < 3:
        return None
    series = list(values)
    result = []
    for _ in range(horizon):
        value = max(0, sum(series[-3:]) / 3)
        result.append(round(value))
        series.append(value)
    return result


def backtest(values):
    if len(values) < 4:
        return None
    errors = [abs(values[i] - sum(values[i - 3:i]) / 3) for i in range(3, len(values))]
    return round(sum(errors) / len(errors), 1)


def validate_filters(months, horizon):
    try:
        months, horizon = int(months), int(horizon)
    except (TypeError, ValueError):
        raise ValueError('Invalid filters')
    if not 3 <= months <= 24 or not 1 <= horizon <= 6:
        raise ValueError('Invalid filters')
    return months, horizon
