import unittest
from unittest.mock import patch
from main import main

class TestMain(unittest.TestCase):
    @patch('src.assistant.FranquinelsonAssistant.chat')
    def test_should_call_chat_when_main_called(self, mock_chat):
        main()
        mock_chat.assert_called_once()

if __name__ == '__main__':
    unittest.main()
