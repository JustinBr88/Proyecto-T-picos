import unittest
from datetime import date

from fancyhotel.forecast import monthly_series, moving_average, backtest, validate_filters


class ForecastTests(unittest.TestCase):
    def test_month_boundary_and_duplicate_room_nights(self):
        stays = [
            (1, date(2026, 1, 30), date(2026, 2, 2), 'A', 101),
            (2, date(2026, 1, 31), date(2026, 2, 2), 'A', 101),
        ]
        result = monthly_series(stays, {'A': 2}, date(2026, 1, 1), date(2026, 3, 1))
        self.assertEqual([row['room_nights'] for row in result], [2, 1])
        self.assertEqual([row['reservations'] for row in result], [2, 2])
        self.assertEqual(result[0]['rooms'], 1)
        self.assertEqual(result[0]['occupancy_percent'], round(200 / 62, 1))

    def test_empty_period_and_insufficient_history(self):
        result = monthly_series([], {'A': 1}, date(2026, 1, 1), date(2026, 4, 1))
        self.assertEqual([row['room_nights'] for row in result], [0, 0, 0])
        self.assertIsNone(moving_average([1, 2], 3))

    def test_year_boundary_and_checkout_exclusive(self):
        result = monthly_series([
            (1, date(2025, 12, 31), date(2026, 1, 2), 'A', 101),
            (2, date(2025, 12, 30), date(2026, 1, 1), 'A', 102),
        ], {'A': 2}, date(2025, 12, 1), date(2026, 2, 1))
        self.assertEqual([row['month'] for row in result], ['2025-12', '2026-01'])
        self.assertEqual([row['room_nights'] for row in result], [3, 1])
        self.assertEqual([row['reservations'] for row in result], [2, 1])

    def test_forecast_and_backtest(self):
        self.assertEqual(moving_average([9, 9, 9], 3), [9, 9, 9])
        self.assertEqual(moving_average([0, 0, 0], 1), [0])
        self.assertEqual(backtest([9, 9, 9, 9]), 0)

    def test_invalid_filters(self):
        self.assertEqual(validate_filters('12', '3'), (12, 3))
        for months, horizon in [('a', 3), (2, 3), (25, 3), (12, 0), (12, 7)]:
            with self.assertRaises(ValueError):
                validate_filters(months, horizon)


if __name__ == '__main__':
    unittest.main()
