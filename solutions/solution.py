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

def recommend(user_id: int, k: int) -> List[int]:
    """
      Раскомментируй и пиши код здесь
      Возвращает список из k item_id, рекомендованных пользователю.
      user_id - пользователь, для которого подбираются рекоммендации
      k - число соседей   
    """
    global user_item_matrix, item_similarity, users, items
    """Возвращает список из k item_id, рекомендованных пользователю."""
    if user_id not in users:
        return []

    user_idx = np.where(users == user_id)[0][0]
    user_ratings = user_item_matrix[user_idx].toarray().flatten()

    # Индексы фильмов, которые пользователь еще не оценил
    unrated_items = np.where(user_ratings == 0)[0]

    if len(unrated_items) == 0:
        return []

    # Предсказываем рейтинги для неоцененных фильмов
    pred_ratings = []
    for item_idx in unrated_items:
        # Находим индексы фильмов, которые пользователь оценил
        rated_items = np.where(user_ratings > 0)[0]

        # Берем top-5 наиболее похожих фильмов из оцененных пользователем
        sim_scores = item_similarity[item_idx, rated_items]
        top_k_indices = np.argsort(sim_scores)[-5:]
        top_k_sim = sim_scores[top_k_indices]
        top_k_ratings = user_ratings[rated_items[top_k_indices]]

        # Взвешенное среднее с учетом схожести
        if top_k_sim.sum() > 0:
            pred_rating = np.dot(top_k_sim, top_k_ratings) / top_k_sim.sum()
        else:
            pred_rating = 0

        pred_ratings.append((items[item_idx], pred_rating))

    # Сортируем по предсказанному рейтингу и возвращаем top-k
    pred_ratings.sort(key=lambda x: x[1], reverse=True)
    return [item for item, _ in pred_ratings[:k]]

def predict(user_id: int, item_id: int) -> float:
    """Предсказывает рейтинг для пары пользователь-фильм."""
    global user_item_matrix, item_similarity, users, items
    if user_id not in users or item_id not in items:
        return 0.0

    user_idx = np.where(users == user_id)[0][0]
    item_idx = np.where(items == item_id)[0][0]

    user_ratings = user_item_matrix[user_idx].toarray().flatten()
    rated_items = np.where(user_ratings > 0)[0]

    if len(rated_items) == 0:
        return 0.0

    # Берем top-5 наиболее похожих фильмов из оцененных пользователем
    sim_scores = item_similarity[item_idx, rated_items]
    top_k_indices = np.argsort(sim_scores)[-5:]
    top_k_sim = sim_scores[top_k_indices]
    top_k_ratings = user_ratings[rated_items[top_k_indices]]

    # Взвешенное среднее с учетом схожести
    if top_k_sim.sum() > 0:
        pred_rating = np.dot(top_k_sim, top_k_ratings) / top_k_sim.sum()
    else:
        pred_rating = 0.0

    return pred_rating


def evaluate(test_data: pd.DataFrame) -> float:
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