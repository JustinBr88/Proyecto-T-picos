"""Consultas de habitaciones y disponibilidad.

Dos estadías se solapan si `res.checkin_date < checkout AND res.checkout_date > checkin`:
es la misma regla que `fancyhotel.availability.overlaps` (ver sus tests).
"""
from fancyhotel.db.connection import get_db


def search_rooms(location, checkin_date, checkout_date):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            """SELECT location, room_number, type, room_cost, capacity, extra_bed_price
            FROM Room
            WHERE (location, room_number) NOT IN (
                SELECT r.location, r.room_number
                FROM Room AS r
                JOIN (Reserves_Extra_Bed AS bed, Reservation AS res)
                ON bed.location = r.location AND bed.room_number = r.room_number
                    AND res.reservation_id = bed.reservation_id
                WHERE res.checkin_date < %(checkoutDate)s AND res.checkout_date > %(checkinDate)s
                    AND res.cancelled_or_not = 0
            ) AND location = %(location)s""",
            {"location": location, "checkinDate": checkin_date, "checkoutDate": checkout_date},
        )
        rooms = [
            {
                "location": location,
                "room_number": room_number,
                "room_type": room_type,
                "cost": cost,
                "capacity": capacity,
                "extra_bed_price": extra_bed_price,
            }
            for (location, room_number, room_type, cost, capacity, extra_bed_price) in cursor.fetchall()
        ]
        return {"response": rooms, "result": len(rooms) > 0}
    finally:
        cursor.close()


def is_room_free(room_number, location, checkin_date, checkout_date, exclude_reservation=-1):
    """`exclude_reservation` deja afuera la propia reserva al cambiarle las fechas."""
    cursor = get_db().cursor()
    try:
        cursor.execute(
            """SELECT r.location, r.room_number
            FROM Room AS r
            JOIN (Reserves_Extra_Bed AS bed, Reservation AS res)
            ON bed.location = r.location
                AND bed.room_number = r.room_number
                AND res.reservation_id = bed.reservation_id
            WHERE r.room_number = %(room_number)s
                AND r.location = %(location)s
                AND res.checkin_date < %(checkoutDate)s
                AND res.checkout_date > %(checkinDate)s
                AND res.cancelled_or_not = 0
                AND res.reservation_id != %(exclude_reservation)s""",
            {"room_number": room_number, "location": location, "checkinDate": checkin_date,
             "checkoutDate": checkout_date, "exclude_reservation": exclude_reservation},
        )
        return len(cursor.fetchall()) == 0
    finally:
        cursor.close()


def count_rooms(location):
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Room WHERE location = %(location)s", {"location": location})
        (count,) = cursor.fetchone()
        return count
    finally:
        cursor.close()


def get_stays(location, start_date, end_date):
    """Reservas activas de la locación que ocupan alguna noche de [start_date, end_date).

    Devuelve tuplas (locación, habitación, check-in, check-out).
    """
    cursor = get_db().cursor()
    try:
        cursor.execute(
            """SELECT bed.location, bed.room_number, res.checkin_date, res.checkout_date
            FROM Reservation AS res
            JOIN Reserves_Extra_Bed AS bed ON bed.reservation_id = res.reservation_id
            WHERE bed.location = %(location)s
                AND res.cancelled_or_not = 0
                AND res.checkin_date < %(end)s
                AND res.checkout_date > %(start)s""",
            {"location": location, "start": start_date, "end": end_date},
        )
        return cursor.fetchall()
    finally:
        cursor.close()
