import pandas as pd
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Глобальные переменные
tfidf_matrix = None
movie_ids = []
movie_index = {}
similarity_matrix = None

def fit(train_data: pd.DataFrame) -> None:
    """
    Обучает модель на взаимодействиях и текстовых признаках.
    """
    global tfidf_matrix, movie_ids, movie_index, similarity_matrix

    # Запоминаем movie_ids и индексы
    movie_ids = train_data['movie_id'].tolist()
    movie_index = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}

    # Объединяем жанры в текст для векторизации
    genre_texts = train_data['genres'].fillna('').astype(str)

    # Векторизация с помощью TF-IDF
    vectorizer = TfidfVectorizer(token_pattern=r'[^|]+')
    tfidf_matrix = vectorizer.fit_transform(genre_texts)

    # Вычисляем косинусное сходство между всеми фильмами
    similarity_matrix = cosine_similarity(tfidf_matrix)

def recommend(movie_id: int, k: int) -> List[int]:
    """
    Возвращает список из k фильмов, рекомендованных к просмотру
    вместе с заданным фильмом movie_id.
    """
    if movie_id not in movie_index:
        return []

    idx = movie_index[movie_id]
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    
    # Сортируем по убыванию схожести, исключая сам фильм
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommended = [movie_ids[i] for i, score in similarity_scores if i != idx][:k]
    
    return recommended

def evaluate(test_data: pd.DataFrame, relevant_genres=['Crime']) -> float:
    """
    Оценивает модель на тестовой выборке и возвращает precision@5.
    """
    relevant_movies = test_data[test_data['genres'].str.contains('|'.join(relevant_genres), na=False)]
    relevant_movie_ids = set(relevant_movies['movie_id'])

    precision_scores = []

    for movie_id in test_data['movie_id']:
        recommended = recommend(movie_id, 5)
        if not recommended:
            continue
        hits = sum(1 for rec_id in recommended if rec_id in relevant_movie_ids)
        precision = hits / 5
        precision_scores.append(precision)

    if not precision_scores:
        return 0.0

    return np.mean(precision_scores)
