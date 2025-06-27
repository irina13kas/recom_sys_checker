import random
from typing import Tuple, Dict

def generate() -> Tuple[str, Dict]:
    cf_part = random.choice(["SVD", "ALS"])
    cb_part = random.choice(["TF-IDF", "count-based"])
    strategy = random.choice(["взвешенное среднее", "усреднение", "модель обучения ранжированию"])
    metric = random.choice(["precision@5", "recall@5", "RMSE"])
    dataset = random.choice(["hybrid_movies.csv", "hybrid_books.csv"])

    task_text = f"""Тип задачи: Гибридная рекомендательная система

        📘 Описание:
        Реализуйте гибридную рекомендательную систему, объединяющую:
        - Коллаборативную часть: {cf_part} (использует рейтинги)
        - Контентную часть: {cb_part} (использует описания объектов)

        Метод объединения предсказаний: **{strategy}**.

        📂 Входные данные:
        - Датасет: `{dataset}`, содержащий `user_id`, `item_id`, `rating`, `title`, `description`.

        🎯 Цель:
        Оцените модель с помощью метрики **{metric}** (на предсказании рейтингов или релевантности).

        ✔️ Требования к структуре кода:
        - Реализуйте следующие функции:

        ```python
        def fit(train_data: pd.DataFrame) -> None:
            \"\"\"Обучает обе части модели: коллаборативную и контентную.\"\"\"

        def predict(user_id: int, item_id: int) -> float:
            \"\"\"Предсказывает рейтинг пользователя user_id для item_id.\"\"\"
        📎 Условия:

        Решение должно быть реализовано в одном файле solution.py.

        Разрешается использовать библиотеки: pandas, numpy, sklearn, surprise, lightfm.
        """
    task_info = {
        "type": "hybrid",
        "cf_algorithm": cf_part,
        "cb_algorithm": cb_part,
        "combination_strategy": strategy,
        "metric": metric,
        "dataset": dataset
        }

    return task_text, task_info