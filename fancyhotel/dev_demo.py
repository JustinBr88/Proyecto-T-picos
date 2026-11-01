"""Fill an entirely empty local Fancy_Hotel database with labelled demo data.

This command never drops tables or adds rows to a populated database. Its
generated records are for development only and must not be treated as bookings
made by actual customers.
"""
import os

from fancyhotel import create_app
from fancyhotel.db.connection import get_db
from fancyhotel.db.seed import seed_database


TABLES = ("Manager", "Customer", "Credit_Card", "Room", "Reservation",
          "Reserves_Extra_Bed", "Review")


def prepare_demo():
    password = os.getenv("DEV_MANAGER_PASSWORD", "")
    if not 8 <= len(password) <= 16:
        raise RuntimeError("DEV_MANAGER_PASSWORD must contain 8–16 characters")

    app = create_app()
    if app.config["DB_NAME"] != "Fancy_Hotel" or app.config["TEST_DB_NAME"] == app.config["DB_NAME"]:
        raise RuntimeError("This command only prepares the separate Fancy_Hotel development database")

    with app.app_context():
        cursor = get_db().cursor()
        try:
            counts = {}
            for table in TABLES:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()[0]
        finally:
            cursor.close()
        if any(counts.values()):
            raise RuntimeError(f"Refusing to change a nonempty database: {counts}")

        result = seed_database(history_months=15, manager_password=password)
        print("DEMO DATA ONLY in Fancy_Hotel; manager username: Madmn")
        print(result)


if __name__ == "__main__":
    try:
        prepare_demo()
    except RuntimeError as error:
        raise SystemExit(str(error)) from None
