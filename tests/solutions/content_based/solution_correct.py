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

    movie_ids = train_data['movie_id'].tolist()
    movie_index = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}

    genre_texts = train_data['genres'].fillna('').astype(str)

    vectorizer = TfidfVectorizer(token_pattern=r'[^|]+')
    tfidf_matrix = vectorizer.fit_transform(genre_texts)

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
    
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommended = [movie_ids[i] for i, score in similarity_scores if i != idx][:k]
    
    return recommended

def evaluate(test_data: pd.DataFrame, relevant_genres='Crime') -> float:
    # Создаем копию, чтобы не изменять исходные данные
    test_data = test_data.copy()
    
    # Разделяем жанры и приводим к нижнему регистру
    test_data['genres'] = test_data['genres'].apply(
        lambda x: [genre.strip().lower() for genre in str(x).split('|')]
    )
    
    # Получаем список релевантных фильмов
    relevant_items = test_data[
        test_data['genres'].apply(lambda genres: relevant_genres.lower() in genres)
    ]['movie_id'].tolist()
    
    # Получаем рекомендации для первого пользователя (возможно, нужно переделать)
    recs = recommend(test_data['movie_id'][0], 5)
    print(recs)
    # Вычисляем Precision@5
    if not recs:  # если нет рекомендаций
        return 0.0
    
    relevant_in_recs = len(set(recs) & set(relevant_items))
    precision = relevant_in_recs / len(recs)  # делим на количество рекомендаций
    
    return round(precision, 2)

test = pd.DataFrame([
        {"movie_id": 250, "genres": 'Action|Fantasy'},  # не релевантный
        {"movie_id": 251, "genres": 'Drama'},  # не релевантный
        {"movie_id": 260, "genres": 'Thriller|Crime'},  # релевантный
        {"movie_id": 266, "genres": 'Comedy|Romance|Crime'},  # релевантный
        {"movie_id": 280, "genres": 'Sci-Fi'}  # не релевантный
    ])

fit(test)
print(evaluate(test))

