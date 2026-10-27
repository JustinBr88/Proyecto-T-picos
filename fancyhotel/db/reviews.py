"""Consultas de reseñas."""
from fancyhotel.db.connection import get_db


def add_review(username, location, comment, rating):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO Review (location, comment, rating, username)
            VALUES (%(location)s, %(comment)s, %(rating)s, %(username)s)""",
            {"location": location, "comment": comment, "rating": rating, "username": username},
        )
        if cursor.rowcount == 0:
            return "Could not create review", False
        db.commit()
        return "Review created", True
    finally:
        cursor.close()


def get_reviews(location):
    cursor = get_db().cursor()
    try:
        cursor.execute(
            "SELECT review_id, location, comment, rating, username FROM Review WHERE location = %(location)s",
            {"location": location},
        )
        return [
            {
                "review_id": review_id,
                "location": location,
                "comment": comment,
                "rating": rating,
                "username": username,
            }
            for (review_id, location, comment, rating, username) in cursor.fetchall()
        ]
    finally:
        cursor.close()
