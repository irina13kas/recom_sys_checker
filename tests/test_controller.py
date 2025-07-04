import unittest
from unittest.mock import patch, MagicMock, mock_open
import pytest
import time
import io
from controller import TaskService


class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.service = TaskService()

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

    @patch("controller.save_report_to_csv", return_value="exported/path/report.csv")
    def test_export_report(self, mock_save):
        mock_save.return_value = "report.csv"
        service = TaskService()

        result = service.export_report("Some report", path="custom.csv")
        self.assertEqual(result, "report.csv")
        mock_save.assert_called_once_with("Some report", "custom.csv")

    @patch("controller.generate_report", return_value="Dummy report content")
    def test_generate_and_validate_stress(self, mock_generate_report):
        mock_generate_report.return_value = "Dummy report content"

        num_iterations = 10000
        start_time = time.time()

        for _ in range(num_iterations):
            task_text, task_info = self.service.generate_task()
            self.assertIsNotNone(task_text)
            self.assertIsNotNone(task_info)

            fake_solution_code = b"def solution():\n    return 42"
            from io import BytesIO
            fake_file = BytesIO(fake_solution_code)
            self.service.upload_solution(fake_file)

            report = self.service.validate_solution()
            self.assertEqual(report, "Dummy report content")

        end_time = time.time()
        duration = end_time - start_time

        print(f"\nExecuted {num_iterations} iterations in {duration:.2f} seconds")

        self.assertLess(duration, 20, "Тест выполняется слишком долго")



if __name__ == "__main__":
    unittest.main()
