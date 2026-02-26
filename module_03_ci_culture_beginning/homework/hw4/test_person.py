import unittest
from datetime import datetime
from person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.p = Person("Иван", 1990, "ул. Ленина, д.1")

    def test_init(self):
        self.assertEqual(self.p.name, "Иван")
        self.assertEqual(self.p.yob, 1990)
        self.assertEqual(self.p.address, "ул. Ленина, д.1")

    def test_get_age(self):
        current_year = datetime.now().year
        expected = current_year - 1990
        self.assertEqual(self.p.get_age(), expected)

    def test_get_name(self):
        self.assertEqual(self.p.get_name(), "Иван")

    def test_set_name(self):
        self.p.set_name("Петр")
        self.assertEqual(self.p.name, "Петр")

    def test_set_address(self):
        self.p.set_address("ул. Пушкина, д.2")
        self.assertEqual(self.p.address, "ул. Пушкина, д.2")

    def test_get_address(self):
        self.assertEqual(self.p.get_address(), "ул. Ленина, д.1")

    def test_is_homeless_false(self):
        self.assertFalse(self.p.is_homeless())

    def test_is_homeless_true(self):
        p2 = Person("Анна", 2000, "")
        self.assertTrue(p2.is_homeless())


if __name__ == '__main__':
    unittest.main()