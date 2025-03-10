import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.state_manager import StateManager
import json

class TestStateManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_should_save_state_successfully_given_valid_context(self, mock_file):
        state_manager = StateManager("state.json", debug=True)
        state_manager.save_state({"key": "value"})

        mock_file.assert_called_with("state.json", 'w', encoding='utf-8')
        self.assertTrue(mock_file.called)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"context": {"key": "value"}}')
    def test_should_load_state_successfully_given_file_exists(self, mock_file, mock_exists):
        state_manager = StateManager("state.json", debug=True)
        context = state_manager.load_state()

        mock_file.assert_called_with("state.json", 'r', encoding='utf-8')
        self.assertEqual(context, {"key": "value"})

    @patch("os.path.exists", return_value=False)
    def test_should_return_none_when_load_state_given_no_file(self, mock_exists):
        state_manager = StateManager("state.json", debug=True)
        context = state_manager.load_state()

        self.assertIsNone(context)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=IOError("Erro ao ler arquivo"))
    def test_should_handle_exception_when_loading_state_given_ioerror(self, mock_file, mock_exists):
        state_manager = StateManager("state.json", debug=True)
        context = state_manager.load_state()

        self.assertIsNone(context)

if __name__ == '__main__':
    unittest.main()
