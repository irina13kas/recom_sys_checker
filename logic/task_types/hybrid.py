import random
from typing import Tuple, Dict

class HybridTaskGenerator:
    def __init__(self):
        self.cf_parts = ["SVD", "ALS"]
        self.cb_parts = ["TF-IDF", "count-based"]
        self.metrics = ["precision@5", "recall@5", "RMSE"]
        self.datasets = ["fashion_products.csv"]
    
    def generate_task(self) -> Tuple[str, Dict]:

        cf_part = random.choice(self.cf_parts)
        cb_part = random.choice(self.cb_parts)
        metric = random.choice(self.metrics)
        dataset = random.choice(self.datasets)

        task_text = f"""Тип задачи: Гибридная рекомендательная система

            📘 Описание:
            Реализуйте гибридную рекомендательную систему, объединяющую:
            - Коллаборативную часть user_based: {cf_part} (использует рейтинги)
            - Контентную часть: {cb_part} (использует описания объектов)

            📂 Входные данные:
            - Датасет: `{dataset}`, содержащий `user_id`, `product_id`, `product_name`, `brand`, `category`,
            `price`, `rating`, `color`, `size`.

            🎯 Цель:
            Оцените модель с помощью метрики **{metric}** (на предсказании рейтингов или релевантности).

            ✔️ Требования к структуре кода:
            - Реализуйте следующие функции:

            def fit(train_data: pd.DataFrame) -> None:
                \"\"\"Обучает обе части модели: коллаборативную и контентную.\"\"\"

            def recommend(user_id: int, k = 5) -> List[int]:
                \"\"\"Возвращает список из k item_id, рекомендованных пользователю.\"\"\"
            
            def evaluate(test_data: pd.DataFrame, relevant_rating = 4, brand = 'Gucci') -> float:
                \"\"\"Оценивает модель на тестовой выборке и возвращает значение метрики (например, RMSE, precision@5).\"\"\"
            📎 Условия:

            Решение должно быть реализовано в одном файле solution.py.

            Разрешается использовать библиотеки: pandas, numpy, sklearn, surprise, lightfm.
            """
        task_info = {
            "type": "hybrid",
            "cf_algorithm": cf_part,
            "cb_algorithm": cb_part,
            "metric": metric,
            "dataset": dataset
            }

        return task_text, task_info