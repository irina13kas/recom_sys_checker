import unittest
from logic.task_types.collaborative import CollaborativeTaskGenerator
from logic.task_types.content_based import ContentBasedTaskGenerator
from logic.task_types.hybrid import HybridTaskGenerator

class TestCollaborativeTaskGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = CollaborativeTaskGenerator()

    def test_generate_task_output_structure(self):
        task_text, task_info = self.generator.generate_task()
        self.assertIsInstance(task_text, str)
        self.assertIsInstance(task_info, dict)

    def test_generate_task_contains_all_keys(self):
        _, task_info = self.generator.generate_task()
        expected_keys = {"type", "filter_type", "algorithm", "metric", "k", "dataset"}
        self.assertTrue(expected_keys.issubset(task_info.keys()))

    def test_generate_task_values_in_allowed_ranges(self):
        _, task_info = self.generator.generate_task()
        self.assertIn(task_info["type"], ["collaborative"])
        self.assertIn(task_info["filter_type"], self.generator.filter_types)
        self.assertIn(task_info["algorithm"], self.generator.algorithms)
        self.assertIn(task_info["metric"], self.generator.algorithm_metric_map[task_info["algorithm"]])
        self.assertIn(task_info["k"], self.generator.k_values)
        self.assertIn(task_info["dataset"], self.generator.datasets)

    def test_generate_task_multiple_runs(self):
        for _ in range(100):
            try:
                self.generator.generate_task()
            except Exception as e:
                self.fail(f"generate_task() вызвал исключение: {e}")

class TestContentBasedTaskGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ContentBasedTaskGenerator()

    def test_generate_task_returns_expected_structure(self):
        task_text, task_info = self.generator.generate_task()
        self.assertIsInstance(task_text, str, "task_text должен быть строкой")
        self.assertIsInstance(task_info, dict, "task_info должен быть словарём")

    def test_task_info_contains_required_keys(self):
        _, task_info = self.generator.generate_task()
        expected_keys = {"type", "algorithm", "metric", "dataset"}
        self.assertTrue(expected_keys.issubset(task_info.keys()), "task_info должен содержать все необходимые ключи")

    def test_values_are_valid(self):
        _, task_info = self.generator.generate_task()
        self.assertEqual(task_info["type"], "content_based", "Тип должен быть 'content_based'")
        self.assertIn(task_info["algorithm"], self.generator.algorithms, "algorithm не входит в допустимые значения")
        self.assertIn(task_info["metric"], self.generator.algorithm_metric_map[task_info["algorithm"]], "metric не соответствует выбранному algorithm")
        self.assertIn(task_info["dataset"], self.generator.datasets, "dataset не входит в допустимые значения")

    def test_generate_task_multiple_runs(self):
        for _ in range(100):
            try:
                self.generator.generate_task()
            except Exception as e:
                self.fail(f"generate_task() вызвал исключение: {e}")

class TestHybridTaskGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = HybridTaskGenerator()

    def test_generate_task_returns_expected_structure(self):
        task_text, task_info = self.generator.generate_task()
        self.assertIsInstance(task_text, str, "task_text должен быть строкой")
        self.assertIsInstance(task_info, dict, "task_info должен быть словарём")

    def test_task_info_contains_required_keys(self):
        _, task_info = self.generator.generate_task()
        expected_keys = {"type", "cf_algorithm", "cb_algorithm", "metric", "dataset"}
        self.assertTrue(expected_keys.issubset(task_info.keys()), "task_info должен содержать все необходимые ключи")

    def test_values_are_valid(self):
        _, task_info = self.generator.generate_task()
        self.assertEqual(task_info["type"], "hybrid", "Тип должен быть 'hybrid'")
        self.assertIn(task_info["cf_algorithm"], self.generator.cf_parts, "cf_algorithm не входит в допустимые значения")
        self.assertIn(task_info["cb_algorithm"], self.generator.cb_parts, "cb_algorithm не входит в допустимые значения")
        self.assertIn(task_info["metric"], self.generator.metrics, "metric не входит в допустимые значения")
        self.assertIn(task_info["dataset"], self.generator.datasets, "dataset не входит в допустимые значения")

    def test_generate_task_multiple_runs(self):
        for _ in range(1000):
            try:
                self.generator.generate_task()
            except Exception as e:
                self.fail(f"generate_task() вызвал исключение: {e}")

if __name__ == '__main__':
    unittest.main()
