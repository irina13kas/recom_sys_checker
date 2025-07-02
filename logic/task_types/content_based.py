import random
from typing import Tuple, Dict


class ContentBasedTaskGenerator:
    def __init__(self):   
        self.algorithms = ["TF-IDF", "count-based", "cosine similarity"]
        self.metric = ["precision@5", "recall@5", "NDCG"]
        self.algorithm_metric_map = {
            "TF-IDF": ["NDCG", "precision@5"],
            "count-based": ["recall@5","precision@5"],
            "cosine similarity": ["NDCG","precision@5"]
        }
        self.datasets = ["movies_content.csv"]#, "video_game_content.csv"])

    def generate_task(self) -> Tuple[str, Dict]:

        algorithm = random.choice(self.algorithms)
        metric = random.choice(self.algorithm_metric_map[algorithm])
        dataset = random.choice(self.datasets)

        task_text = f"""Тип задачи: Контентная рекомендательная система

            📘 Описание:
            Реализуйте рекомендательную систему на основе контентных признаков, используя метод {algorithm}.
            Система должна анализировать текстовые описания объектов и предсказывать наиболее релевантные пользователю элементы.

            📂 Входные данные:
            - Датасет: `{dataset}`, содержащий `movie_id`, `title`, `genres`.
            - Используйте описания объектов для извлечения признаков, а взаимодействия — для обучения.

            🎯 Цель:
            Оцените рекомендации с помощью метрики **{metric}**.

            ✔️ Требования к структуре кода:
            - Реализуйте следующие функции:

            def fit(train_data: pd.DataFrame) -> None:
                \"\"\"Обучает модель на взаимодействиях и текстовых признаках.\"\"\"

            def recommend(movie_id: int, k = 5) -> List[int]:
                \"\"\"Возвращает список из k фильмов, рекомендованных к просмотру вместе с заданным фильмом movie_id.\"\"\"

            def evaluate(test_data: pd.DataFrame, relevant_genres = 'Crime') -> float:
                \"\"\"Оценивает модель на тестовой выборке и возвращает значение метрики (например, precision@5).\"\"\"

            📎 Условия:
            Решение должно быть реализовано в одном файле solution.py.

            Разрешается использовать библиотеки: pandas, numpy, sklearn."""
        
        task_info = {
            "type": "content_based",
            "algorithm": algorithm,
            "metric": metric,
            "dataset": dataset
            }

        return task_text, task_info