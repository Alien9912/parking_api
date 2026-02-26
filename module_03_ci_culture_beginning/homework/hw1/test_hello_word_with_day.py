import unittest
from freezegun import freeze_time
from hello_word_with_day import app

class TestGoodDay(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @freeze_time("2025-03-24")
    def test_monday(self):
        resp = self.client.get('/hello-world/Иван')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Хорошего понедельника', resp.text)
        self.assertIn('Иван', resp.text)

    @freeze_time("2025-03-25")
    def test_tuesday(self):
        resp = self.client.get('/hello-world/Маша')
        self.assertIn('Хорошего вторника', resp.text)

    @freeze_time("2025-03-26")
    def test_wednesday(self):
        resp = self.client.get('/hello-world/Петя')
        self.assertIn('Хорошей среды', resp.text)

    @freeze_time("2025-03-27")
    def test_thursday(self):
        resp = self.client.get('/hello-world/Оля')
        self.assertIn('Хорошего четверга', resp.text)

    @freeze_time("2025-03-28")
    def test_friday(self):
        resp = self.client.get('/hello-world/Коля')
        self.assertIn('Хорошей пятницы', resp.text)

    @freeze_time("2025-03-29")
    def test_saturday(self):
        resp = self.client.get('/hello-world/Юля')
        self.assertIn('Хорошей субботы', resp.text)

    @freeze_time("2025-03-30")
    def test_sunday(self):
        resp = self.client.get('/hello-world/Дима')
        self.assertIn('Хорошего воскресенья', resp.text)

    def test_name_with_greeting(self):
        with freeze_time("2025-03-26"):
            resp = self.client.get('/hello-world/Хорошей%20среды')
            self.assertIn('Хорошей среды', resp.text)

if __name__ == '__main__':
    unittest.main()