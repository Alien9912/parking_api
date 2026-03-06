import unittest
from block_errors import BlockErrors


class BlockErrorsTestCase(unittest.TestCase):
    def test_error_ignored(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0
        except Exception:
            self.fail("Exception should have been ignored")

    def test_error_propagated(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0

    def test_nested_blocks(self):
        try:
            with BlockErrors({TypeError}):
                with BlockErrors({ZeroDivisionError}):
                    a = 1 / '0'
        except Exception:
            self.fail("TypeError should have been ignored by outer block")

    def test_child_errors_ignored(self):
        try:
            with BlockErrors({Exception}):
                a = 1 / 0
        except Exception:
            self.fail("Child exception should be ignored because parent is in list")

    def test_multiple_errors(self):
        try:
            with BlockErrors({ZeroDivisionError, TypeError}):
                a = 1 / 0
        except Exception:
            self.fail("Exception should be ignored")
        try:
            with BlockErrors({ZeroDivisionError, TypeError}):
                a = 1 / '0'
        except Exception:
            self.fail("Exception should be ignored")


if __name__ == '__main__':
    unittest.main()