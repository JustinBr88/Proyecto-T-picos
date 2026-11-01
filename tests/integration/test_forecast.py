"""HU3 HTTP → MySQL → forecast; uses only the isolated test database."""
from datetime import date, timedelta

import pytest

from fancyhotel.db.connection import get_db
from tests.support import CUSTOMER, MANAGER

pytestmark = pytest.mark.integration


def previous_month(day):
    return (day - timedelta(days=1)).replace(day=1)


def test_forecast_reads_real_rows_and_excludes_cancellations(client, app):
    current = date.today().replace(day=1)
    months = [previous_month(current)]
    months.insert(0, previous_month(months[0]))
    months.insert(0, previous_month(months[0]))
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        for month in months:
            cursor.execute("""INSERT INTO Reservation
                (checkin_date, checkout_date, username, card_number, cancelled_or_not)
                VALUES (%s, %s, %s, NULL, '0')""",
                (month, month + timedelta(days=1), CUSTOMER['username']))
            cursor.execute("INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id) VALUES ('Atlanta', 101, %s)",
                           (cursor.lastrowid,))
        cursor.execute("""INSERT INTO Reservation
            (checkin_date, checkout_date, username, card_number, cancelled_or_not)
            VALUES (%s, %s, %s, NULL, '1')""",
            (months[-1], months[-1] + timedelta(days=1), CUSTOMER['username']))
        cursor.execute("INSERT INTO Reserves_Extra_Bed (location, room_number, reservation_id) VALUES ('Atlanta', 101, %s)",
                       (cursor.lastrowid,))
        db.commit()
        cursor.close()

    assert client.get('/api/reports/forecast').status_code == 403
    assert client.post('/api/login', json=MANAGER).status_code == 200
    response = client.get('/api/reports/forecast?location=Atlanta&type=Standard&months=3&horizon=3')
    assert response.status_code == 200, response.get_json()
    payload = response.get_json()
    assert [row['room_nights'] for row in payload['history']] == [1, 1, 1]
    assert [row['reservations'] for row in payload['history']] == [1, 1, 1]
    assert [row['room_nights'] for row in payload['forecast']] == [1, 1, 1]
    assert all(row['capacity_room_nights'] >= 28 for row in payload['history'])
    suite = client.get('/api/reports/forecast?location=Atlanta&type=Suite&months=3')
    assert suite.status_code == 200
    assert all(row['room_nights'] == 0 for row in suite.get_json()['history'])
    assert suite.get_json()['insufficient_data']
    assert client.get('/api/reports/forecast?months=0').status_code == 400
    assert client.get('/api/reports/forecast?location=Unknown').status_code == 400


def test_customer_cannot_read_forecast(client):
    assert client.post('/api/login', json={"username": CUSTOMER['username'],
                                           "password": CUSTOMER['password']}).status_code == 200
    assert client.get('/api/reports/forecast').status_code == 403
