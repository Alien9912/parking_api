import unittest
from accounting import app, storage


class TestFinance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        storage.clear()
        storage['20250301'] = 1500
        storage['20250315'] = 2300
        storage['20250410'] = 3200
        storage['20241220'] = 5000
        storage['20260105'] = 700

    def setUp(self):
        self.client = app.test_client()

    def test_add_valid_date(self):
        resp = self.client.get('/add/20260310/4500')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('20260310', storage)
        self.assertEqual(storage['20260310'], 4500)

    def test_add_invalid_date_format_should_fail(self):
        resp = self.client.get('/add/2025-03-01/1000')
        self.assertEqual(resp.status_code, 404)

    def test_add_negative_amount(self):
        resp = self.client.get('/add/20260311/-500')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('20260311', storage)
        self.assertEqual(storage['20260311'], -500)

    def test_calculate_year_existing(self):
        resp = self.client.get('/calculate/2025')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode(), '12000')

    def test_calculate_year_empty(self):
        resp = self.client.get('/calculate/2027')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode(), '0')

    def test_calculate_month_existing(self):
        resp = self.client.get('/calculate/2025/3')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode(), '3800')

    def test_calculate_month_empty(self):
        resp = self.client.get('/calculate/2025/2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode(), '0')

    def test_calculate_month_invalid_month(self):
        resp = self.client.get('/calculate/2025/13')
        self.assertEqual(resp.status_code, 404)

    def test_add_when_storage_empty(self):
        storage.clear()
        resp = self.client.get('/add/20260808/999')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('20260808', storage)
        self.assertEqual(storage['20260808'], 999)

    def test_calculate_when_storage_empty(self):
        storage.clear()
        resp = self.client.get('/calculate/2025')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode(), '0')


if __name__ == '__main__':
    unittest.main()