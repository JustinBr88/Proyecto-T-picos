"""HTTP contract checks without touching the development database."""
import unittest
from datetime import date
from unittest.mock import patch

from fancyhotel import create_app
from fancyhotel.api import reports


class ForecastApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SECRET_KEY': 'test-only-secret'})
        self.client = self.app.test_client()

    def test_anonymous_and_customer_cannot_read_forecast(self):
        self.assertEqual(self.client.get('/api/reports/forecast').status_code, 403)
        with self.client.session_transaction() as session:
            session['username'] = 'Cdemo'
            session['role'] = 'customer'
        self.assertEqual(self.client.get('/api/reports/forecast').status_code, 403)

    def test_manager_filters_and_response(self):
        with self.client.session_transaction() as session:
            session['username'] = 'Madmn'
            session['role'] = 'manager'
        with patch.object(reports.forecast_db, 'has_demo_data', return_value=True), patch.object(reports.forecast_db, 'forecast_data', return_value=({'Atlanta': 2}, ['Atlanta'], ['Standard'], [
                (1, date(2026, 7, 30), date(2026, 8, 2), 'Atlanta', 101)])) as query:
            response = self.client.get('/api/reports/forecast?location=Atlanta&type=Standard&months=12&horizon=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['demonstration_data'])
        self.assertEqual(len(response.json['history']), 12)
        self.assertIn('forecast', response.json)
        self.assertEqual(query.call_args.args[2:], ('Atlanta', 'Standard'))
        self.assertEqual(self.client.get('/api/reports/forecast?months=0').status_code, 400)

    def test_login_creates_server_session_and_frontend_files_are_served(self):
        with patch('fancyhotel.api.auth.users.login', return_value=True):
            response = self.client.post('/api/login', json={'username': 'Madmn', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session:
            self.assertEqual(session['role'], 'manager')
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/static/views/forecast.html').status_code, 200)
        self.assertEqual(self.client.get('/static/js/controllers.js').status_code, 200)

    def test_invalid_type_and_missing_history(self):
        with self.client.session_transaction() as session:
            session['username'] = 'Madmn'
            session['role'] = 'manager'
        with patch.object(reports.forecast_db, 'has_demo_data', return_value=False), patch.object(reports.forecast_db, 'forecast_data', return_value=({'Atlanta': 2}, ['Atlanta'], ['Standard'], [])):
            response = self.client.get('/api/reports/forecast?type=Unknown')
            self.assertEqual(response.status_code, 400)
            response = self.client.get('/api/reports/forecast')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['forecast'], [])
        self.assertTrue(response.json['insufficient_data'])


if __name__ == '__main__':
    unittest.main()
