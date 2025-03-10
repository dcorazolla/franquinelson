import unittest
from unittest.mock import patch, MagicMock
from src.assistant import FranquinelsonAssistant

class TestFranquinelsonAssistant(unittest.TestCase):

    @patch('src.assistant.ModelLoader')
    @patch('src.assistant.StateManager')
    @patch('src.assistant.PromptBuilder')
    @patch('src.assistant.CommandExecutor')
    @patch('src.assistant.TaskExecutor')
    def test_should_initialize_all_components_when_assistant_created(
        self, mock_task_executor, mock_command_executor, 
        mock_prompt_builder, mock_state_manager, mock_model_loader
    ):
        assistant = FranquinelsonAssistant()
        mock_model_loader.assert_called_once()
        mock_prompt_builder.assert_called_once()
        mock_command_executor.assert_called_once()
        mock_task_executor.assert_called_once()
        mock_state_manager.assert_called_once()

if __name__ == '__main__':
    unittest.main()
