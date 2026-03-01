import unittest
from decrypt import decrypt

class TestDecoder(unittest.TestCase):
    def test_one_dot_at_end(self):
        cases = [
            ("абра-кадабра.", "абра-кадабра"),
            ("привет.", "привет"),
        ]
        for enc, expected in cases:
            with self.subTest(enc=enc):
                self.assertEqual(decrypt(enc), expected)

    def test_two_dots_remove_prev_char(self):
        cases = [
            ("абраа..-кадабра", "абра-кадабра"),
            ("1..2.3", "23"),
            ("а..б", "б"),
        ]
        for enc, expected in cases:
            with self.subTest(enc=enc):
                self.assertEqual(decrypt(enc), expected)

    def test_three_dots_remove_one_char(self):
        cases = [
            ("123...45", "1245"),
            ("абрау...-кадабра", "абра-кадабра"),
        ]
        for enc, expected in cases:
            with self.subTest(enc=enc):
                self.assertEqual(decrypt(enc), expected)

    def test_mixed_dots_and_hyphens(self):
        cases = [
            ("абраа..-.кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
            ("а---..б", "а--б"),
        ]
        for enc, expected in cases:
            with self.subTest(enc=enc):
                self.assertEqual(decrypt(enc), expected)

    def test_only_dots(self):
        cases = [
            ("абра........", ""),
            (".", ""),
            ("1.......................", ""),
            ("..........", ""),
        ]
        for enc, expected in cases:
            with self.subTest(enc=enc):
                self.assertEqual(decrypt(enc), expected)

    def test_empty_string(self):
        self.assertEqual(decrypt(""), "")

if __name__ == '__main__':
    unittest.main()