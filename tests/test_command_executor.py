import unittest
import subprocess
from unittest.mock import patch, MagicMock
from src.command_executor import CommandExecutor

class TestCommandExecutor(unittest.TestCase):

    def setUp(self):
        self.executor = CommandExecutor(debug=True)

    def test_should_extract_command_successfully_when_valid_response_given(self):
        response = "Execute isso {command: ls -l}"
        command = self.executor.extract_command(response)
        self.assertEqual(command, "ls -l")

    def test_should_return_none_when_no_command_given(self):
        response = "Nenhum comando aqui"
        command = self.executor.extract_command(response)
        self.assertIsNone(command)

    @patch('subprocess.run')
    def test_should_execute_allowed_command_successfully(self, mock_run):
        mock_result = MagicMock(stdout="output", stderr="")
        mock_run.return_value = mock_result

        result = self.executor.execute_command("ls -l")
        self.assertEqual(result, "output")
        mock_run.assert_called_once()

    def test_should_return_error_when_command_not_allowed(self):
        result = self.executor.execute_command("rm -rf /")
        self.assertEqual(result, "Erro: comando não permitido 🚫")

    @patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd='ls', timeout=10))
    def test_should_handle_timeout_exception(self, mock_run):
        result = self.executor.execute_command("ls -l")
        self.assertEqual(result, "Erro: tempo limite excedido para execução do comando ⌛️")

if __name__ == '__main__':
    unittest.main()
