"""Reportes para managers.

Los tres reportes están fijados a agosto y septiembre (requisito del proyecto
original). Tenerlo en cuenta en el Caso 3 (previsión de demanda).
"""
from fancyhotel.db.connection import get_db


def reservation_report():
    """Cantidad de reservas por mes y locación."""
    cursor = get_db().cursor()
    try:
        cursor.execute(
            """SELECT MONTH(checkin_date), bed.location, COUNT(*)
            FROM Reservation AS res
            JOIN (Reserves_Extra_Bed AS bed) ON res.reservation_id = bed.reservation_id
            WHERE MONTH(res.checkin_date) = 8 OR MONTH(res.checkin_date) = 9
            GROUP BY MONTH(checkin_date), bed.location"""
        )
        report = {}
        for month, location, count in cursor.fetchall():
            report.setdefault(month, {})[location] = count
        return report
    finally:
        cursor.close()


def room_report():
    """Categoría de habitación más reservada por locación (agosto)."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """CREATE OR REPLACE VIEW reservation_by_category AS (
                SELECT MONTH(res.checkin_date) AS mth, room.type AS type, room.location AS location,
                    COUNT(room.type) AS cnt
                FROM Room AS room
                JOIN (Reserves_Extra_Bed AS bed, Reservation AS res)
                ON room.location = bed.location AND room.room_number = bed.room_number
                    AND res.reservation_id = bed.reservation_id
                WHERE MONTH(res.checkin_date) = 8
                GROUP BY MONTH(res.checkin_date), room.location, room.type)"""
        )
        db.commit()

        cursor.execute(
            """SELECT rbc.mth, rbc.location, rbc.type, rbc.cnt
            FROM reservation_by_category AS rbc
            INNER JOIN (
                SELECT mth, location, MAX(cnt) AS cnt
                FROM reservation_by_category
                GROUP BY mth, location
            ) AS groupedrbc
            ON rbc.mth = groupedrbc.mth AND rbc.location = groupedrbc.location AND rbc.cnt = groupedrbc.cnt"""
        )
        report = {}
        for month, location, room_type, count in cursor.fetchall():
            report.setdefault(month, {}).setdefault(location, []).append({"type": room_type, "count": count})
        return report
    finally:
        cursor.close()


def revenue_report():
    """Ingresos por mes y locación."""
    cursor = get_db().cursor()
    try:
        cursor.execute(
            """SELECT MONTH(res.checkin_date) AS month, room.location AS location, SUM(res.total_cost)
            FROM Room AS room
            JOIN (Reserves_Extra_Bed AS bed, Reservation AS res)
            ON room.location = bed.location AND room.room_number = bed.room_number
                AND res.reservation_id = bed.reservation_id
            WHERE MONTH(res.checkin_date) = 8 OR MONTH(res.checkin_date) = 9
            GROUP BY MONTH(res.checkin_date), room.location"""
        )
        report = {}
        for month, location, cost in cursor.fetchall():
            report.setdefault(month, {})[location] = cost
        return report
    finally:
        cursor.close()
