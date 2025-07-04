import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
from typing import List

# ===реализуй данные функции===
item_similarity = None
user_item_matrix = None
items = None
users = None

def fit(train_data: pd.DataFrame) -> None:
    """
      Раскомментируй и пиши код здесь
      Обучает модель на тренировочном датасет
      train_data - данные для обучения       
    """
    """Обучает модель на тренировочном датасете."""
    # Создаем user-item матрицу
    global user_item_matrix, item_similarity, users, items
    users = train_data['user_id'].unique()
    items = train_data['item'].unique()

    # Создаем разреженную матрицу пользователь-фильм
    user_to_idx = {user: idx for idx, user in enumerate(users)}
    item_to_idx = {item: idx for idx, item in enumerate(items)}

    rows = train_data['user_id'].map(user_to_idx)
    cols = train_data['item'].map(item_to_idx)
    ratings = train_data['rating']

    user_item_matrix = csr_matrix((ratings, (rows, cols)),
                                        shape=(len(users), len(items)))

    # Вычисляем косинусную схожесть между фильмами (аналог Pearson)
    item_similarity = cosine_similarity(user_item_matrix.T)
#возвращаем пустой массив
def recommend(user_id: int, k: int) -> List[int]:
    return []

def predict(user_id: int, item_id: int) -> float:
    return 0.0


def evaluate(test_data: pd.DataFrame, relevant_rating = 4) -> float:
    """
      Раскомментируй и пиши код здесь
      Оценивает модель на тестовой выборке и возвращает значение метрики (например, RMSE, precision@2).
      test_data - данные для рассчета метрики  
    """
    """Оценивает модель на тестовой выборке и возвращает RMSE."""
    y_true = []
    y_pred = []

    for _, row in test_data.iterrows():
        user_id = row['user_id']
        item_id = row['item']
        true_rating = row['rating']

        pred_rating = predict(user_id, item_id)

        y_true.append(true_rating)
        y_pred.append(pred_rating)

    return sqrt(mean_squared_error(y_true, y_pred))



# Если тебе потребуются дополнительные функции, можешь смело их добавлять, они не будут учитываться при проверке.
# Тебе предложен датасет для проверки работы твоей программы, его можно скачать на той же странице, что и этот файл