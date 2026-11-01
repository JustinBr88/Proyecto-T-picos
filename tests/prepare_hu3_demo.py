"""Add labelled HU3 demo stays to an empty isolated test database only.

Run after integration tests: they recreate Fancy_Hotel_test before each test.
Never run against the development database.
"""
from datetime import date, timedelta

from fancyhotel import create_app
from fancyhotel.config import Config
from fancyhotel.db.connection import get_db


def previous_month(day):
    return (day - timedelta(days=1)).replace(day=1)


def main():
    if Config.TEST_DB_NAME == Config.DB_NAME or not Config.TEST_DB_NAME.endswith('_test'):
        raise RuntimeError('Demo requires a distinct database ending in _test')
    app = create_app({'DB_NAME': Config.TEST_DB_NAME, 'SECRET_KEY': 'local-demo-only'})
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT COUNT(*) FROM Reservation')
            if cursor.fetchone()[0] != 0:
                raise RuntimeError('Test database already has reservations; demo data was not inserted')
            cursor.execute("SELECT COUNT(*) FROM Manager WHERE username = 'Mtest'")
            if cursor.fetchone()[0] != 1:
                raise RuntimeError('Run isolated integration tests first to prepare fixture accounts')
            cursor.execute("SELECT COUNT(*) FROM Room WHERE location = 'Atlanta' AND room_number = 101")
            if cursor.fetchone()[0] != 1:
                raise RuntimeError('Test fixture rooms are missing')
            cursor.execute("""INSERT INTO Room (location, room_number, type, room_cost, capacity, extra_bed_price)
                VALUES ('Miami', 201, 'Standard', 120, 2, 15)""")
            current = date.today().replace(day=1)
            months = [previous_month(current)]
            months.insert(0, previous_month(months[0]))
            months.insert(0, previous_month(months[0]))
            for index, month in enumerate(months, 1):
                for location, number, nights in [('Atlanta', 101, index), ('Miami', 201, index + 1)]:
                    cursor.execute("""INSERT INTO Reservation
                        (checkin_date, checkout_date, username, card_number, cancelled_or_not)
                        VALUES (%s, %s, 'Ctest', NULL, '0')""",
                        (month, month + timedelta(days=nights)))
                    cursor.execute("""INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id)
                        VALUES (%s, %s, %s)""", (location, number, cursor.lastrowid))
            cursor.execute("""INSERT INTO Reservation
                (checkin_date, checkout_date, username, card_number, cancelled_or_not)
                VALUES (%s, %s, 'Ctest', NULL, '1')""",
                (months[-1], months[-1] + timedelta(days=2)))
            cursor.execute("""INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id)
                VALUES ('Atlanta', 101, %s)""", (cursor.lastrowid,))
            db.commit()
            print('HU3 demo only:', Config.TEST_DB_NAME, '3 completed months, 2 locations, 1 cancellation')
        except Exception:
            db.rollback()
            raise
        finally:
            cursor.close()


if __name__ == '__main__':
    main()
