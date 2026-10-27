"""Consultas de habitaciones y disponibilidad."""
from fancyhotel.db.connection import get_db


def search_rooms(location, checkin_date, checkout_date):
    # BUG-1 (se corrige en el Caso 2): sólo considera ocupadas las reservas
    # contenidas por completo en el rango buscado, no los solapamientos parciales.
    cursor = get_db().cursor()
    try:
        cursor.execute(
            """SELECT *
            FROM Room
            WHERE (location, room_number) NOT IN (
                SELECT r.location, r.room_number
                FROM Room AS r
                JOIN (Reserves_Extra_Bed AS bed, Reservation AS res)
                ON bed.location = r.location AND bed.room_number = r.room_number
                    AND res.reservation_id = bed.reservation_id
                WHERE res.checkin_date >= %(checkinDate)s AND res.checkout_date <= %(checkoutDate)s
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


def is_room_free(room_number, location, checkin_date, checkout_date, exclude_reservation):
    # BUG-1: misma condición de solapamiento incompleta que search_rooms.
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
                AND res.checkin_date >= %(checkinDate)s
                AND res.checkout_date <= %(checkoutDate)s
                AND res.cancelled_or_not = 0
                AND res.reservation_id != %(exclude_reservation)s""",
            {"room_number": room_number, "location": location, "checkinDate": checkin_date,
             "checkoutDate": checkout_date, "exclude_reservation": exclude_reservation},
        )
        return len(cursor.fetchall()) == 0
    finally:
        cursor.close()
