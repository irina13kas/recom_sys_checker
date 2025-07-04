import unittest
from unittest.mock import patch, mock_open
from report_csv import save_report_to_csv


class TestSaveReportToCSV(unittest.TestCase):

    @patch("report_csv.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_report_to_csv_with_path(self, mock_file, mock_makedirs):
        report_text = "Line 1\nLine 2\nLine 3"
        path = "reports/custom_report.csv"

        result_path = save_report_to_csv(report_text, path)

        mock_makedirs.assert_called_once_with("reports", exist_ok=True)
        mock_file.assert_called_once_with(path, mode="w", encoding="utf-8", newline='')

        # Проверяем, что write вызывался (т.к. csv.writer использует его многократно)
        self.assertTrue(mock_file().write.call_count > 0)
        self.assertEqual(result_path, path)

    @patch("report_csv.datetime")
    @patch("report_csv.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_report_to_csv_without_path(self, mock_file, mock_makedirs, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "2025-07-04_12-00-00"
        report_text = "One\nTwo"
        
        result_path = save_report_to_csv(report_text)

        expected_path = "reports/report_2025-07-04_12-00-00.csv"
        mock_file.assert_called_once_with(expected_path, mode="w", encoding="utf-8", newline='')

        self.assertTrue(result_path.endswith(".csv"))
        self.assertIn("report_2025-07-04_12-00-00", result_path)

    @patch("report_csv.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_report_content_written(self, mock_file, mock_makedirs):
        report = "Header line\nTest passed\nAnother line"
        save_report_to_csv(report, path="reports/test.csv")

        handle = mock_file()
        # csv.writer вызывает write много раз, поэтому проверим, что среди всех записанных байтов есть "Test passed"
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        self.assertIn("Test passed", written_content)


if __name__ == "__main__":
    unittest.main()
