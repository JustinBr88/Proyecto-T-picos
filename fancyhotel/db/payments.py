"""Consultas de tarjetas de crédito."""
from fancyhotel.db.connection import get_db


def add_credit_card(username, card_number, cvv, expiration_date, card_name):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO Credit_Card (card_number, name, cvv, expiration_date, username)
            VALUES (%(card_number)s, %(name)s, %(cvv)s, %(expiration_date)s, %(username)s)""",
            {"card_number": card_number, "name": card_name, "cvv": cvv,
             "expiration_date": expiration_date, "username": username},
        )
        if cursor.rowcount == 0:
            return "Credit card creation failed", False
        db.commit()
        return "Credit card successfully created", True
    finally:
        cursor.close()


def get_credit_cards(username):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            "SELECT card_number, name, cvv, expiration_date, username FROM Credit_Card WHERE username = %(username)s",
            {"username": username},
        )
        return [
            {
                "card_number": card_number,
                "name": name,
                "cvv": cvv,
                "expiration_date": str(expiration_date),
                "username": username,
            }
            for (card_number, name, cvv, expiration_date, username) in cursor.fetchall()
        ]
    finally:
        cursor.close()


def delete_credit_card(username, card_number):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM Credit_Card WHERE card_number = %(card_number)s AND username = %(username)s",
            {"card_number": card_number, "username": username},
        )
        if cursor.rowcount == 0:
            return "This credit card was not found", False
        db.commit()
        return "Credit card deleted", True
    finally:
        cursor.close()
