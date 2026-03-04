import unittest
import shutil
from remote_execution import app


class RemoteExecutionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False

    def test_valid_code(self):
        response = self.app.post('/run_code', data={
            'code': 'print("Hello, World!")',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('result', data)
        self.assertEqual(data['result'].strip(), 'Hello, World!')

    def test_timeout_exceeded(self):
        response = self.app.post('/run_code', data={
            'code': 'import time; time.sleep(2); print("Done")',
            'timeout': 1
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result'], 'Timeout exceeded. Process terminated.')

    def test_invalid_timeout(self):
        response = self.app.post('/run_code', data={
            'code': 'print("test")',
            'timeout': 0
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('errors', data)

    def test_missing_code(self):
        response = self.app.post('/run_code', data={
            'timeout': 5
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('errors', data)

    @unittest.skipIf(not shutil.which('prlimit'), "prlimit not available, skipping security test")
    def test_shell_injection_attempt(self):
        code = 'print("Hello"); import os; os.system("echo hacked")'
        response = self.app.post('/run_code', data={
            'code': code,
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('result', data)
        self.assertNotIn('hacked', data['result'])


if __name__ == '__main__':
    unittest.main()