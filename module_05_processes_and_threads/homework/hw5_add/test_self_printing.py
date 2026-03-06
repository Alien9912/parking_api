import unittest
import subprocess


class SelfPrintingTestCase(unittest.TestCase):
    def test_self_printing(self):
        result = subprocess.run(
            ['python', 'self_printing.py'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        output = result.stdout
        with open('self_printing.py', 'r', encoding='utf-8') as f:
            expected = f.read()
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()