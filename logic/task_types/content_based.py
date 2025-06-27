import random
from typing import Tuple, Dict

def generate() -> Tuple[str, Dict]:
    algo = random.choice(["TF-IDF", "count-based", "cosine similarity"])
    metric = random.choice(["precision@5", "recall@5", "MAE", "NDCG"])
    dataset = random.choice(["movie_content.csv", "video_game_content.csv"])

    task_text = f"""Тип задачи: Контентная рекомендательная система

        📘 Описание:
        Реализуйте рекомендательную систему на основе контентных признаков, используя метод {algo}.
        Система должна анализировать текстовые описания объектов и предсказывать наиболее релевантные пользователю элементы.

        📂 Входные данные:
        - Датасет: `{dataset}`, содержащий `item_id`, `title`, `description`, `user_id`, `rating`.
        - Используйте описания объектов для извлечения признаков, а взаимодействия — для обучения.

        🎯 Цель:
        Оцените рекомендации с помощью метрики **{metric}**.

        ✔️ Требования к структуре кода:
        - Реализуйте следующие функции:

        ```python
        def fit(train_data: pd.DataFrame) -> None:
            \"\"\"Обучает модель на взаимодействиях и текстовых признаках.\"\"\"

        def recommend(user_id: int, k: int) -> List[int]:
            \"\"\"Возвращает список из k item_id, рекомендованных пользователю.\"\"\"

        📎 Условия:
        Решение должно быть реализовано в одном файле solution.py.

        Разрешается использовать библиотеки: pandas, numpy, sklearn.
        """
    
    task_info = {
        "type": "content",
        "algorithm": algo,
        "metric": metric,
        "dataset": dataset
        }

    return task_text, task_info