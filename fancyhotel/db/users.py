"""Consultas de clientes (Customer) y managers (Manager)."""
from fancyhotel.db.connection import get_db


def user_exists(username):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            "SELECT username FROM Customer WHERE username = %(username)s",
            {"username": username},
        )
        return len(cursor.fetchall()) != 0
    finally:
        cursor.close()


def email_exists(email):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            "SELECT email FROM Customer WHERE email = %(email)s",
            {"email": email},
        )
        return len(cursor.fetchall()) != 0
    finally:
        cursor.close()


def register_user(username, email, password, first_name, last_name):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO Customer (username, email, password, first_name, last_name)
            VALUES (%(username)s, %(email)s, %(password)s, %(first_name)s, %(last_name)s)""",
            {"username": username, "email": email, "password": password,
             "first_name": first_name, "last_name": last_name},
        )
        if cursor.rowcount == 1:
            db.commit()
    finally:
        cursor.close()


def login(username, password):
    """El rol se deduce de la primera letra del usuario: C = cliente, M = manager."""
    tables = {"C": "Customer", "M": "Manager"}
    table = tables.get(username[:1])
    if table is None:
        return False

    cursor = get_db().cursor()
    try:
        cursor.execute(
            f"SELECT * FROM {table} WHERE username = %(username)s AND password = %(password)s",
            {"username": username, "password": password},
        )
        return len(cursor.fetchall()) != 0
    finally:
        cursor.close()
