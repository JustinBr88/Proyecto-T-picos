"""Read only data access for the demand forecast."""
from fancyhotel.db.connection import get_db


def has_demo_data():
    """Identify the existing development seed by its reserved customer email."""
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT 1 FROM Customer WHERE username = %s AND email = %s LIMIT 1",
                       ("Cdemo", "demo@fancyhotel.test"))
        return cursor.fetchone() is not None
    finally:
        cursor.close()


def forecast_data(start, end, location=None, room_type=None):
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT DISTINCT location FROM Room ORDER BY location")
        locations = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT DISTINCT type FROM Room ORDER BY type")
        room_types = [row[0] for row in cursor.fetchall()]
        params = {"location": location, "room_type": room_type, "start": start, "end": end}
        cursor.execute("""SELECT location, COUNT(*) FROM Room
            WHERE (%(location)s IS NULL OR location = %(location)s)
              AND (%(room_type)s IS NULL OR type = %(room_type)s)
            GROUP BY location""", params)
        capacities = dict(cursor.fetchall())
        cursor.execute("""SELECT res.reservation_id, res.checkin_date, res.checkout_date,
                   bed.location, bed.room_number
            FROM Reservation AS res
            JOIN Reserves_Extra_Bed AS bed ON bed.reservation_id = res.reservation_id
            JOIN Room AS room ON room.location = bed.location AND room.room_number = bed.room_number
            WHERE res.cancelled_or_not = '0'
              AND res.checkin_date < %(end)s AND res.checkout_date > %(start)s
              AND (%(location)s IS NULL OR bed.location = %(location)s)
              AND (%(room_type)s IS NULL OR room.type = %(room_type)s)""", params)
        return capacities, locations, room_types, cursor.fetchall()
    finally:
        cursor.close()
