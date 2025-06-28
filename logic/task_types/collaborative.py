import random
from typing import Dict, Tuple

class CollaborativeTaskGenerator:
    def __init__(self):
        self.filter_types = ["user_based", "item_based"]
        self.algorithms = ["k-NN", "SVD", "ALS"]
        self.algorithm_metric_map = {
            "k-NN": ["precision@2", "recall@3"],
            "SVD": ["RMSE"],
            "ALS": ["RMSE"]
        }
        self.k_values = [5, 10, 20]
        self.datasets = ["movie_ratings.csv"] #, "games_collaborative.csv"]

    def generate_task(self) -> Tuple[str, Dict]:
        filter_type = random.choice(self.filter_types)
        algorithm = random.choice(self.algorithms)
        metric = random.choice(self.algorithm_metric_map[algorithm])
        k = random.choice(self.k_values)
        dataset = random.choice(self.datasets)

        task_text = f"""Тип задачи: Коллаборативная фильтрация ({filter_type})

        📘 Описание:
        Реализуйте рекомендательную систему с использованием метода {filter_type} фильтрации.
        Используйте алгоритм {algorithm} числом соседей k = {k}.

        📂 Входные данные:
        - Датасет: `{dataset}` с колонками `user_id`, `item`, `rating`.
        - Модель должна быть обучена перед вызовом функции рекомендаций.

        🎯 Цель:
        Оцените результат с помощью метрики **{metric}** на тестовой выборке.

        ✔️ Требования к структуре кода:
        - Реализуйте следующие функции:

        def fit(train_data: pd.DataFrame) -> None:
            \"\"\"Обучает модель на тренировочном датасете.\"\"\"

        def recommend(user_id: int, k: int) -> List[int]:
            \"\"\"Возвращает список из k item_id, рекомендованных пользователю.\"\"\"

        def evaluate(test_data: pd.DataFrame) -> float:
            \"\"\"Оценивает модель на тестовой выборке и возвращает значение метрики (например, RMSE, precision@5).\"\"\"
            
        📎 Условия:
        Решение должно быть реализовано в одном файле solution.py.

        Разрешается использовать библиотеки: pandas, numpy, sklearn, surprise."""

        task_info = {
            "type": "collaborative",
            "filter_type": filter_type,
            "algorithm": algorithm,
            "metric": metric,
            "k": k,
            "dataset": dataset
        }

        return task_text, task_info
