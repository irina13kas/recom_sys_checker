import pandas as pd
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import ndcg_score

# Глобальные переменные для модели
tfidf = TfidfVectorizer()
movie_data = None
tfidf_matrix = None
cosine_sim = None
movie_to_index = {}

def fit(train_data: pd.DataFrame) -> None:
    """
    Обучает модель на тренировочном датасете
    train_data - данные для обучения (должен содержать колонки 'movie_id' и 'genres')
    """
    global movie_data, tfidf_matrix, cosine_sim, movie_to_index
    
    movie_data = train_data.copy()
    # Преобразуем жанры в строку, разделенную пробелами (если они в формате списка)
    if isinstance(movie_data['genres'].iloc[0], list):
        movie_data['genres'] = movie_data['genres'].apply(lambda x: ' '.join(x))
    
    # Обучаем TF-IDF на жанрах
    tfidf_matrix = tfidf.fit_transform(movie_data['genres'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    movie_to_index = {movie_id: idx for idx, movie_id in enumerate(movie_data['movie_id'])}

def recommend(movie_id: int, k: int) -> List[int]:
    """
    Возвращает список из k фильмов, рекомендованных к просмотру вместе с заданным фильмом
    movie_id - ID фильма, для которого ищем рекомендации
    k - количество рекомендаций
    """
    if movie_id not in movie_to_index:
        return []
    
    idx = movie_to_index[movie_id]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:k+1]  # Исключаем сам фильм
    movie_indices = [i[0] for i in sim_scores]
    return movie_data.iloc[movie_indices]['movie_id'].tolist()

def evaluate(test_data: pd.DataFrame, relevant_genre: str = 'Crime') -> float:
    """
    Оценивает модель на тестовой выборке с помощью NDCG@k
    test_data - данные для оценки (должен содержать колонку 'movie_id')
    relevant_genre - жанр, который считается релевантным
    """
    if movie_data is None:
        return 0.0
    