import unittest
from unittest.mock import patch, MagicMock
from logic import validator
import time
from logic.validator import run_pytest, run_flake8, run_black_check, generate_report


class TestValidator(unittest.TestCase):

    @patch("logic.validator.subprocess.run")
    def test_run_pytest_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        task_info = {"type": "content_based", "algorithm": "TF-IDF", "metric": "NDCG", "dataset": "movies_content.csv"}

        result = run_pytest(task_info)
        self.assertIn("✅", result)

    @patch("logic.validator.subprocess.run")
    def test_run_pytest_failure(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="E       AssertionError: expected 2, got 1\n",
            stderr=""
        )
        task_info = {"type": "collaborative", "algorithm": "ALS", "metric": "precision@5", "dataset": "movie_lens.csv"}

        result = run_pytest(task_info)
        self.assertIn("❌", result)
        self.assertIn("AssertionError", result)

    @patch("logic.validator.subprocess.run")
    def test_run_flake8_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        result = run_flake8("fake_path.py")
        self.assertIn("✅ flake8", result)

    @patch("logic.validator.subprocess.run")
    def test_run_flake8_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="fake_path.py:1:1: F401 'os' imported but unused\n")
        result = run_flake8("fake_path.py")
        self.assertIn("❌ flake8", result)
        self.assertIn("F401", result)

    @patch("logic.validator.subprocess.run")
    def test_run_black_check_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        result = run_black_check("fake_path.py")
        self.assertIn("✅ black", result)

    @patch("logic.validator.subprocess.run")
    def test_run_black_check_failure(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="would reformat fake_path.py\n"
        )
        result = run_black_check("fake_path.py")
        self.assertIn("❌ black", result)
        self.assertIn("would reformat", result)

    @patch("logic.validator.run_pytest")
    @patch("logic.validator.run_flake8")
    @patch("logic.validator.run_black_check")
    def test_generate_report(self, mock_black, mock_flake8, mock_pytest):
        mock_pytest.return_value = "✅ Все тесты пройдены успешно!"
        mock_flake8.return_value = "✅ flake8: Стиль кода соответствует стандарту.\n"
        mock_black.return_value = "✅ black: Форматирование корректное.\n"

        task_info = {"type": "hybrid", "algorithm": "weighted_sum", "metric": "recall@5", "dataset": "movies_content.csv"}

        report = generate_report(task_info)
        self.assertIn("✅ Все тесты пройдены успешно!", report)
        self.assertIn("flake8", report)
        self.assertIn("black", report)

    @patch("logic.validator.subprocess.run")
    def test_generate_report_stress(self, mock_subprocess_run):

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "All good!"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        task_info_example = {
            "type": "collaborative",
            "name": "test_task",
            "params": {"n_users": 10, "n_items": 5}
        }

        n_runs = 10000
        start_time = time.time()

        for i in range(n_runs):
            with self.subTest(i=i):
                report = validator.generate_report(task_info_example)
                self.assertIn("🧪 Функциональные тесты", report)
                self.assertIn("✅ flake8", report)
                self.assertIn("✅ black", report)

        total_time = time.time() - start_time
        print(f"\n⏱️ Выполнено {n_runs} проверок за {total_time:.2f} секунд.")


if __name__ == "__main__":
    unittest.main()
