import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
import signal
from app import get_pids, free_port, run


class TestApp(unittest.TestCase):
    @patch('app.subprocess.check_output')
    def test_get_pids_success(self, mock_check_output):
        mock_check_output.return_value = "1234\n5678\n"
        pids = get_pids(5000)
        self.assertEqual(pids, [1234, 5678])
        mock_check_output.assert_called_once_with(
            ['lsof', '-t', '-i', ':5000'], text=True, stderr=subprocess.DEVNULL
        )

    @patch('app.subprocess.check_output', side_effect=subprocess.CalledProcessError(1, 'cmd'))
    def test_get_pids_no_processes(self, mock_check_output):
        pids = get_pids(5000)
        self.assertEqual(pids, [])

    @patch('app.os.kill')
    @patch('app.get_pids', return_value=[1234, 5678])
    def test_free_port(self, mock_get_pids, mock_kill):
        free_port(5000)
        mock_kill.assert_any_call(1234, signal.SIGTERM)
        mock_kill.assert_any_call(5678, signal.SIGTERM)
        self.assertEqual(mock_kill.call_count, 2)

    @patch('app.os.kill', side_effect=ProcessLookupError)
    @patch('app.get_pids', return_value=[1234])
    def test_free_port_process_lookup_error(self, mock_get_pids, mock_kill):
        try:
            free_port(5000)
        except Exception:
            self.fail("free_port raised exception on ProcessLookupError")

    @patch('app.os.kill', side_effect=PermissionError)
    @patch('app.get_pids', return_value=[1234])
    def test_free_port_permission_error(self, mock_get_pids, mock_kill):
        with patch('builtins.print') as mock_print:
            free_port(5000)
            mock_print.assert_called_with("Permission denied to kill PID 1234")

    @patch('app.free_port')
    @patch('app.app.run')
    def test_run(self, mock_run, mock_free_port):
        run(5000)
        mock_free_port.assert_called_once_with(5000)
        mock_run.assert_called_once_with(port=5000)


if __name__ == '__main__':
    unittest.main()