import unittest
from unittest.mock import patch, MagicMock
from src.task_executor import TaskExecutor

class TestTaskExecutor(unittest.TestCase):

    def setUp(self):
        self.assistant_mock = MagicMock()
        self.task_executor = TaskExecutor(self.assistant_mock, debug=True)

    @patch('src.task_executor.re.findall')
    def test_should_return_subtasks_list_when_splitting_large_task(self, mock_findall):
        mock_response = {"choices": [{"text": "1. tarefa 1\n2. tarefa 2"}]}
        self.assistant_mock.llm.return_value = mock_response
        mock_findall.return_value = ["tarefa 1", "tarefa 2"]

        subtasks = self.task_executor.split_task("Criar site")
        self.assertEqual(subtasks, ["tarefa 1", "tarefa 2"])

    @patch('src.task_executor.re.findall', return_value=[])
    def test_should_handle_no_subtasks_found_when_split_task_given_invalid_response(self, mock_findall):
        mock_response = {"choices": [{"text": ""}]}
        self.assistant_mock.llm.return_value = mock_response

        subtasks = self.task_executor.split_task("Tarefa vaga")
        self.assertEqual(subtasks, [])

    @patch('builtins.print')
    def test_should_inform_no_subtasks_when_run_full_task_given_no_subtasks_found(self, mock_print):
        self.task_executor.split_task = MagicMock(return_value=[])

        self.task_executor.run_full_task("Nada específico")
        mock_print.assert_called_with("Nenhuma subtarefa identificada.")

    def test_should_execute_each_subtask_when_run_full_task_given_multiple_subtasks(self):
        self.task_executor.split_task = MagicMock(return_value=["sub1", "sub2"])
        self.task_executor.execute_subtask = MagicMock(return_value="OK")

        self.task_executor.run_full_task("Tarefa complexa")

        self.task_executor.execute_subtask.assert_any_call("tarefa complexa")
        self.assertEqual(self.task_executor.execute_subtask.call_count, 2)

if __name__ == '__main__':
    unittest.main()
