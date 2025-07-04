import unittest
import time
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
    
    def test_generate_description_stress(self):
        n_runs = 10000  # количество запусков для нагрузки
        valid_types = {"collaborative", "content_based", "hybrid"}

        start_time = time.time()
        generator = TaskFactory()
        for i in range(n_runs):
            with self.subTest(i=i):
                task_text, task_info = generator.generate_description()

                self.assertIsInstance(task_text, str)
                self.assertIsInstance(task_info, dict)

                self.assertIn("type", task_info)
                self.assertIn(task_info["type"], valid_types)

        total_time = time.time() - start_time
        print(f"\n⏱️ Выполнено {n_runs} вызовов generate_description за {total_time:.2f} секунд.")

if __name__ == '__main__':
    unittest.main()
