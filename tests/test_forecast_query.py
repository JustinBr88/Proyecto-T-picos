import unittest
from datetime import date
from unittest.mock import patch

from fancyhotel.db import forecast


class Cursor:
    def __init__(self):
        self.calls = []
        self.closed = False

    def execute(self, sql, params=None):
        self.calls.append((sql, params))

    def fetchall(self):
        return [[('A',)], [('Standard',)], [('A', 2)], []][len(self.calls) - 1]

    def close(self):
        self.closed = True


class ForecastQueryTests(unittest.TestCase):
    def test_query_filters_cancelled_stays_and_closes_cursor(self):
        cursor = Cursor()
        class Connection:
            def cursor(self):
                return cursor
        with patch.object(forecast, 'get_db', return_value=Connection()):
            capacities, locations, kinds, stays = forecast.forecast_data(date(2026, 1, 1), date(2026, 2, 1), 'A', 'Standard')
        self.assertEqual((capacities, locations, kinds, stays), ({'A': 2}, ['A'], ['Standard'], []))
        sql, params = cursor.calls[-1]
        self.assertIn("res.cancelled_or_not = '0'", sql)
        self.assertIn('res.checkin_date < %(end)s', sql)
        self.assertIn('res.checkout_date > %(start)s', sql)
        self.assertEqual(params['location'], 'A')
        self.assertEqual(params['room_type'], 'Standard')
        self.assertTrue(cursor.closed)


if __name__ == '__main__':
    unittest.main()
