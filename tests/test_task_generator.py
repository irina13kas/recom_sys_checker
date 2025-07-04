import unittest
from logic.task_generator import TaskFactory

class TestTaskFactory(unittest.TestCase):
    def test_generate_description_returns_expected_structure(self):
        task_text, task_info = TaskFactory.generate_description()
        self.assertIsInstance(task_text, str, "task_text должен быть строкой")
        self.assertIsInstance(task_info, dict, "task_info должен быть словарём")

    def test_task_info_contains_type(self):
        _, task_info = TaskFactory.generate_description()
        self.assertIn("type", task_info, "'type' должен присутствовать в task_info")
        self.assertIn(task_info["type"], TaskFactory.GENERATORS.keys(), "Недопустимое значение 'type'")

    def test_task_info_matches_generator_type(self):
        for _ in range(1000):
            _, task_info = TaskFactory.generate_description()
            self.assertIn("type", task_info)
            self.assertIn(task_info["type"], ["collaborative", "content_based", "hybrid"])

if __name__ == '__main__':
    unittest.main()
