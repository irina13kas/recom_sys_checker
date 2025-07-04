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

    # --- Коллаборативная часть (SVD как ALS-альтернатива) ---
    reader = Reader(rating_scale=(train_df.rating.min(), train_df.rating.max()))
    data = Dataset.load_from_df(train_df[['user_id', 'product_id', 'rating']], reader)
    trainset = data.build_full_trainset()

    model = SVD()
    model.fit(trainset)
    collab_model = model

    # --- Контентная часть ---
    products_df['text'] = products_df['product_name'].fillna('') + ' ' + products_df['brand'].fillna('')
    vectorizer = CountVectorizer()
    content_matrix = vectorizer.fit_transform(products_df['text'])
    item_ids = products_df['product_id'].tolist()
    product_ids = products_df['product_id'].values


def recommend(user_id: int, k=5) -> List[int]:
    return []


def evaluate(test_data: pd.DataFrame, relevant_rating=4, brand='Gucci') -> float:
    hits = 0
    total = 0

    test_users = test_data['user_id'].unique()

    for user in test_users:
        actual_items = test_data[(test_data['user_id'] == user) &
                                 (test_data['rating'] >= relevant_rating) &
                                 (test_data['brand'] == brand)]['product_id'].tolist()
        if not actual_items:
            continue

        recommended = recommend(user, k=5)

        hit_count = len(set(actual_items) & set(recommended))
        hits += hit_count
        total += 1

    if total == 0:
        return 0.0
    return hits / total  # precision@5
