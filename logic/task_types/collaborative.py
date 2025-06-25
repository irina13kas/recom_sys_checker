import random
from typing import Dict, Tuple

class CollaborativeTaskGenerator:
    def __init__(self):
        self.filter_types = ["user_based", "item_based"]
        self.algorithms = ["SVD", "ALS", "k-NN"]
        self.metrics = ["precision@5", "recall@5", "RMSE", "NDCG"]
        self.similarities = ["cosine", "pearson"]
        self.k_values = [5, 10, 20]
        self.datasets = ["movie_ratings", "games_collaborative"]

    def generate_task(self) -> Tuple[str, Dict]:
        """Генерирует случайное задание и его параметры."""
        params = {
            "filter_type": random.choice(self.filter_types),
            "algorithm": random.choice(self.algorithms),
            "metric": random.choice(self.metrics),
            "similarity": random.choice(self.similarities),
            "k": random.choice(self.k_values),
            "dataset": random.choice(self.datasets)
        }
        
        task_text = (
            f"Тип задачи: Коллаборативная фильтрация ({params['filter_type']})\n\n"
            f"📘 Описание:\n"
            f"Реализуйте функцию предсказания оценок на основе {params['filter_type']} фильтрации "
            f"с использованием алгоритма {params['algorithm']}.\n\n"
            f"📌 Параметры:\n"
            f"- Количество соседей: k = {params['k']}\n"
            f"- Метрика схожести: {params['similarity']}\n\n"
            f"🎯 Оцените результат с помощью метрики **{params['metric']}**.\n\n"
            f"📎 Датасет: {params['dataset']}.csv"
        )
        
        return task_text, params