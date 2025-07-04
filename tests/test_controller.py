import unittest
from unittest.mock import patch, MagicMock, mock_open
from controller import TaskService


class TestTaskService(unittest.TestCase):

    @patch("controller.TaskFactory.generate_description")
    def test_generate_task(self, mock_generate_description):
        mock_generate_description.return_value = ("Task text", {"type": "hybrid"})
        service = TaskService()
        task_text, task_info = service.generate_task()

        self.assertEqual(task_text, "Task text")
        self.assertEqual(task_info, {"type": "hybrid"})
        self.assertEqual(service.task_text, "Task text")
        self.assertEqual(service.task_info, {"type": "hybrid"})

    @patch("builtins.open", new_callable=mock_open)
    def test_upload_solution(self, mock_file):
        mock_uploaded = MagicMock()
        mock_uploaded.read.return_value = b"print('Hello world')"

        service = TaskService()
        result_path = service.upload_solution(mock_uploaded)

        mock_file.assert_called_once_with("solutions/solution.py", "wb")
        self.assertEqual(result_path, "solutions/solution.py")
        self.assertEqual(service.solution_path, "solutions/solution.py")

    @patch("controller.generate_report")
    def test_validate_solution_success(self, mock_generate_report):
        mock_generate_report.return_value = "✅ All tests passed"
        service = TaskService()
        service.task_info = {"type": "collaborative"}
        service.solution_path = "solutions/solution.py"

        report = service.validate_solution()
        self.assertEqual(report, "✅ All tests passed")
        mock_generate_report.assert_called_once_with(service.task_info)

    def test_validate_solution_missing_info(self):
        service = TaskService()
        service.task_info = None
        service.solution_path = None

        with self.assertRaises(ValueError) as context:
            service.validate_solution()

        self.assertIn("Отсутствуют task_info", str(context.exception))

    @patch("controller.save_report_to_csv")
    def test_export_report(self, mock_save):
        mock_save.return_value = "report.csv"
        service = TaskService()

        result = service.export_report("Some report", path="custom.csv")
        self.assertEqual(result, "report.csv")
        mock_save.assert_called_once_with("Some report", "custom.csv")


if __name__ == "__main__":
    unittest.main()
