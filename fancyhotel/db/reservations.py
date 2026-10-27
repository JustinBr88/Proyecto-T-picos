"""Consultas de reservas."""
from datetime import datetime

from fancyhotel.db.connection import get_db


def _reservation_to_dict(row):
    reservation_id, checkin_date, checkout_date, total_cost, username, card_number, cancelled_or_not = row
    return {
        "reservation_id": reservation_id,
        "checkin_date": str(checkin_date),
        "checkout_date": str(checkout_date),
        "total_cost": total_cost,
        "username": username,
        "card_number": card_number,
        "cancelled_or_not": cancelled_or_not,
    }


def get_rooms_for_reservation(username, reservation_id):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            """SELECT room.location, room.room_number, room.type, room.room_cost, room.capacity,
                room.extra_bed_price, bed.extra_bed_or_not
            FROM Room AS room
            JOIN (Reserves_Extra_Bed AS bed, Reservation AS res)
            ON room.location = bed.location AND room.room_number = bed.room_number
                AND res.reservation_id = bed.reservation_id
            WHERE res.reservation_id = %(reservation_id)s AND res.username = %(username)s""",
            {"reservation_id": reservation_id, "username": username},
        )
        return [
            {
                "location": location,
                "room_number": room_number,
                "room_type": room_type,
                "cost": room_cost,
                "capacity": capacity,
                "extra_bed_price": extra_bed_price,
                "extra_bed_or_not": extra_bed_or_not,
            }
            for (location, room_number, room_type, room_cost, capacity, extra_bed_price,
                 extra_bed_or_not) in cursor.fetchall()
        ]
    finally:
        cursor.close()


def get_reservation(username, reservation_id, include_cancelled):
    query = "SELECT * FROM Reservation WHERE reservation_id = %(reservation_id)s AND username = %(username)s"
    if not include_cancelled:
        query += " AND cancelled_or_not = 0"

    cursor = get_db().cursor()
    try:
        cursor.execute(query, {"reservation_id": reservation_id, "username": username})
        rows = cursor.fetchall()
        if not rows:
            return {}
        reservation = _reservation_to_dict(rows[0])
        reservation["rooms"] = get_rooms_for_reservation(reservation["username"], reservation["reservation_id"])
        return reservation
    finally:
        cursor.close()


def get_reservation_by_card_number(username, card_number):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            "SELECT * FROM Reservation WHERE card_number = %(card_number)s AND username = %(username)s",
            {"card_number": card_number, "username": username},
        )
        return [_reservation_to_dict(row) for row in cursor.fetchall()]
    finally:
        cursor.close()


def insert_reservation(username, checkin_date, checkout_date, card_number, rooms, total_cost):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO Reservation (username, checkin_date, checkout_date, card_number, total_cost)
            VALUES (%(username)s, %(checkin_date)s, %(checkout_date)s, %(card_number)s, %(total_cost)s)""",
            {"username": username, "checkin_date": checkin_date, "checkout_date": checkout_date,
             "card_number": card_number, "total_cost": total_cost},
        )
        reservation_id = cursor.lastrowid

        for room in rooms:
            cursor.execute(
                """INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id, extra_bed_or_not)
                VALUES (%(location)s, %(room_number)s, %(reservation_id)s, %(extra_bed_or_not)s)""",
                {"location": room["location"], "room_number": room["room_number"],
                 "reservation_id": reservation_id, "extra_bed_or_not": room["extra_bed_or_not"]},
            )
            if cursor.rowcount == 0:
                db.rollback()
                return -1, "Error creating reservation", False

        db.commit()
        return reservation_id, "Successfully created reservation", True
    finally:
        cursor.close()


def update_reservation(username, reservation_id, checkin_date, checkout_date, total_cost):
    if not get_reservation(username, reservation_id, False):
        return "This reservation does not exist", False

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """UPDATE Reservation
            SET checkin_date = %(checkin_date)s, checkout_date = %(checkout_date)s, total_cost = %(total_cost)s
            WHERE reservation_id = %(reservation_id)s AND username = %(username)s""",
            {"reservation_id": reservation_id, "checkin_date": checkin_date, "checkout_date": checkout_date,
             "username": username, "total_cost": total_cost},
        )
        db.commit()
        return "Reservation updated", True
    finally:
        cursor.close()


def cancel_reservation(username, reservation_id):
    """Cancela y deja como costo la penalización según los días que faltan para el check-in:
    1 día o menos → 100 %, menos de 4 días → 20 %, más → 0 %."""
    reservation = get_reservation(username, reservation_id, False)
    if not reservation:
        return "This reservation does not exist", False

    checkin_date = datetime.strptime(reservation["checkin_date"], "%Y-%m-%d")
    days_until_checkin = (checkin_date - datetime.now()).days
    if days_until_checkin <= 1:
        total_cost = reservation["total_cost"]
    elif days_until_checkin < 4:
        total_cost = reservation["total_cost"] * 0.20
    else:
        total_cost = 0

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """UPDATE Reservation
            SET cancelled_or_not = 1, total_cost = %(total_cost)s
            WHERE reservation_id = %(reservation_id)s AND username = %(username)s AND cancelled_or_not = 0""",
            {"reservation_id": reservation_id, "username": username, "total_cost": total_cost},
        )
        db.commit()
        if cursor.rowcount > 0:
            return "", True
        return "This reservation has already been cancelled", False
    finally:
        cursor.close()
