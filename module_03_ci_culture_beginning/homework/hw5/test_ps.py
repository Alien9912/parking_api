import unittest
from unittest.mock import patch, MagicMock
import subprocess
from ps import app


class TestPsEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('ps.subprocess.run')
    def test_ps_with_args(self, mock_run):
        mock_process = MagicMock()
        mock_process.stdout = "  PID TTY      STAT   TIME COMMAND\n    1 ?        Ss     0:01 init\n"
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        response = self.client.get('/ps?arg=a&arg=u&arg=x')
        self.assertEqual(response.status_code, 200)
        mock_run.assert_called_once_with(
            ['ps', 'a', 'u', 'x'],
            capture_output=True,
            text=True,
            check=True
        )
        response_text = response.get_data(as_text=True)
        self.assertIn('<pre>', response_text)
        self.assertIn('PID', response_text)

    @patch('ps.subprocess.run')
    def test_ps_no_args(self, mock_run):
        response = self.client.get('/ps')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No arguments provided', response.get_data(as_text=True))
        mock_run.assert_not_called()

    @patch('ps.subprocess.run')
    def test_ps_subprocess_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'ps', stderr='error')
        response = self.client.get('/ps?arg=aux')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error executing ps', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()