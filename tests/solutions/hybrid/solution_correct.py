import pandas as pd
import numpy as np
from typing import List
from surprise import Dataset, Reader, SVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

collab_model = None
user_item_matrix = None
content_matrix = None
item_ids = []
product_ids = []
vectorizer = None
train_df = None
products_df = None

def fit(train_data: pd.DataFrame) -> None:
    global collab_model, user_item_matrix, content_matrix, item_ids, product_ids, vectorizer, train_df, products_df

    train_df = train_data.copy()
    products_df = train_df[['product_id', 'product_name', 'brand']].drop_duplicates()

    # Коллаборативная часть
    reader = Reader(rating_scale=(train_df.rating.min(), train_df.rating.max()))
    data = Dataset.load_from_df(train_df[['user_id', 'product_id', 'rating']], reader)
    trainset = data.build_full_trainset()

    model = SVD()
    model.fit(trainset)
    collab_model = model

    # Контентная часть
    products_df['text'] = products_df['product_name'].fillna('') + ' ' + products_df['brand'].fillna('')
    vectorizer = CountVectorizer()
    content_matrix = vectorizer.fit_transform(products_df['text'])
    item_ids = products_df['product_id'].tolist()
    product_ids = products_df['product_id'].values

def recommend(user_id: int, k=5) -> List[int]:
    global collab_model, train_df, product_ids
    
    # Получаем товары, которые пользователь уже видел
    seen_products = set(train_df[train_df['user_id'] == user_id]['product_id'])
    
    # Все доступные товары (уникальные) минус уже просмотренные
    available_products = list(set(product_ids) - seen_products)  # Убираем дубликаты
    
    if not available_products or k <= 0:
        return []

    # Предсказываем рейтинги для доступных товаров
    predictions = []
    for pid in available_products:
        try:
            pred = collab_model.predict(user_id, pid).est
            predictions.append((pid, pred))
        except:
            continue
    
    # Сортируем по убыванию рейтинга и берем топ-K уникальных товаров
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    # Гарантируем уникальность (на случай, если в predictions попали дубли)
    recommended = []
    seen_pids = set()
    for pid, _ in predictions:
        if pid not in seen_pids:
            recommended.append(pid)
            seen_pids.add(pid)
            if len(recommended) >= k:
                break
    
    return recommended

def evaluate(test_data: pd.DataFrame, relevant_rating=4, brand='Gucci') -> float:
    hits = 0

    test_users = test_data['user_id'].unique()

    recs = recommend(test_users[0])
    hits = test_data[(test_data["rating"] >= 4) & (test_data["brand"] == "Gucci")]["product_id"].unique()
    return len(hits) / len(recs)