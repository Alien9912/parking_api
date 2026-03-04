import unittest
from redirect import Redirect
import sys
from io import StringIO


class RedirectTestCase(unittest.TestCase):
    def test_redirect_stdout(self):
        stdout_buffer = StringIO()
        old_stdout = sys.stdout
        with Redirect(stdout=stdout_buffer):
            print("Hello, stdout!")
        self.assertEqual(stdout_buffer.getvalue().strip(), "Hello, stdout!")
        self.assertIs(sys.stdout, old_stdout)

    def test_redirect_stderr(self):
        stderr_buffer = StringIO()
        old_stderr = sys.stderr
        with Redirect(stderr=stderr_buffer):
            print("Test error", file=sys.stderr)
        self.assertEqual(stderr_buffer.getvalue().strip(), "Test error")
        self.assertIs(sys.stderr, old_stderr)

    def test_redirect_both(self):
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        with Redirect(stdout=stdout_buffer, stderr=stderr_buffer):
            print("Hello stdout")
            print("Hello stderr", file=sys.stderr)
        self.assertEqual(stdout_buffer.getvalue().strip(), "Hello stdout")
        self.assertEqual(stderr_buffer.getvalue().strip(), "Hello stderr")
        self.assertIs(sys.stdout, old_stdout)
        self.assertIs(sys.stderr, old_stderr)

    def test_no_redirect(self):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        with Redirect():
            self.assertIs(sys.stdout, old_stdout)
            self.assertIs(sys.stderr, old_stderr)
        self.assertIs(sys.stdout, old_stdout)
        self.assertIs(sys.stderr, old_stderr)

    def test_only_one_argument(self):
        stdout_buffer = StringIO()
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        with Redirect(stdout=stdout_buffer):
            print("Only stdout")
            self.assertIs(sys.stderr, old_stderr)
        self.assertEqual(stdout_buffer.getvalue().strip(), "Only stdout")
        self.assertIs(sys.stdout, old_stdout)
        self.assertIs(sys.stderr, old_stderr)


if __name__ == '__main__':
    unittest.main()