import pytest
import random
import os
import pandas as pd
import numpy as np
import importlib.util
from pathlib import Path
from typing import List
import math
from sklearn.metrics import mean_squared_error

# task_info = {
#     "type": "content_based",
#     "metric": 'precision@5',
#     }


@pytest.fixture(params=[5, 42, 100, 250])
def generated_dataset(request):
    return get_dummy_data(seed=request.param)

# === Проверка наличия модуля ===
def test_solution_file_exists():
    assert os.path.exists("solutions/solution.py"), "Файл 'solution.py' не найден"

# === Загрузка модуля ===
def load_solution_module():
    path = Path("solutions/solution.py")
    spec = importlib.util.spec_from_file_location("solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# === Расширенные данные ===
def get_dummy_data(seed=None):
    if seed is not None:
        random.seed(seed)

    items = list(range(100, 120))
    genres = ['Adventure', 'Comedy','Romance','Children','Fantasy','Drama','Action','Crime','Thriller','Horror','Mystery','Sci-Fi']
    data = []

    for item in items:
        item_genres = random.sample(genres, k=random.randint(1, 5))
        data.append({
            'movie_id': item,
            'genres': item_genres
        })

    return pd.DataFrame(data)

# === Тесты структуры ===
def test_has_required_functions():
    solution = load_solution_module()
    assert hasattr(solution, 'fit'), "There are no fit"
    assert hasattr(solution, 'recommend'), "There are no recommend"
    assert hasattr(solution, 'evaluate'), "There are no evaluate"

def test_fit_runs_without_error():
    sample_data = get_dummy_data()
    solution = load_solution_module()
    solution.fit(sample_data)

# === Тесты recommend и fit ===
@pytest.mark.parametrize("k", [1, 2, 3])
def test_fit_and_recommend_on_generated(k, generated_dataset):
    solution = load_solution_module()

    solution.fit(generated_dataset)

    movie_id = generated_dataset["movie_id"].iloc[0]
    recs = solution.recommend(movie_id, k=k)
    assert isinstance(recs, list)
    assert len(recs) <= k, f"""
        ❌ Тест не пройден:
        Data: {generated_dataset}
        Expected: {k}
        Actual: {len(recs)}
        """
    assert all(isinstance(mid, int) for mid in recs), f"""
        ❌ Тест не пройден: Все элементы списка должны быть int
        Data: {generated_dataset}
        Expected: all elements int
        """
    assert movie_id not in recs, f"""
        ❌ Тест не пройден: Не следует рекомендовать сам фильм
        Data: {generated_dataset}
        Expected: {recs.remove(movie_id)}
        Actual: {recs}
        """
    assert all(mid in generated_dataset["movie_id"].values for mid in recs), f"""
        ❌ Тест не пройден: Все рекомендованные id должны быть в датасете"
        Data: {generated_dataset}
        Expected: {recs}
        Actual: {generated_dataset["movie_id"].values}
        """
# === Метрики ===

# === Тест precision@5 ===
def test_evaluate_precision_at_5(task_info,
                                  k=5):
    if task_info["metric"] != "precision@5":
        pytest.skip("Метрика в задании не precision@5")
    
    solution = load_solution_module()

    test = pd.DataFrame([
        {"movie_id": 250, "genres": 'Crime'},  # не релевантный
        {"movie_id": 251, "genres": 'Drama|Crime'},  # релевантный
        {"movie_id": 260, "genres": 'Thriller'},  # не релевантный
        {"movie_id": 266, "genres": 'Comedy|Romance'},  # не релевантный
        {"movie_id": 280, "genres": 'Documentary|Drama'} # не релевантный
    ])
    def fake_recommend(movie_id: int, k:int):
        return test["movie_id"].values
    
    solution.recommend = fake_recommend
    recs = fake_recommend(1, 5)
    relevant_items = {251}
    hits = len(set(recs) & relevant_items)
    expected_precision = hits / k

    result = solution.evaluate(test)

    assert isinstance(result, float)
    assert abs(result - expected_precision) < 0.01, f"""
            ❌ Тест не пройден: Сильное расхождение метрики precision@5
            Data: {test}
            Expected: {expected_precision}
            Actual: {result}
            """

# === Тест NDCG ===
def test_evaluate_returns_correct_ndcg_at_k(task_info
                                            ):
    if task_info["metric"] != "NDCG":
        pytest.skip("Метрика в задании не NDCG")
    
    solution = load_solution_module()

    test = pd.DataFrame([
        {"movie_id": 250, "genres": 'Action|Fantasy'},  # не релевантный
        {"movie_id": 251, "genres": 'Drama'},  # не релевантный
        {"movie_id": 260, "genres": 'Thriller|Crime'},  # релевантный
        {"movie_id": 266, "genres": 'Comedy|Romance|Crime'},  # релевантный
        {"movie_id": 280, "genres": 'Sci-Fi'}  # не релевантный
    ])
    solution.fit(test)
    relevance = {0, 0, 1, 1}

    k = 5

    def dcg(relevance_scores, k):
        """
        Вычисляет DCG на первых k позициях.
        relevance_scores — список релевантностей по порядку (0 или 1, или вещественные значения).
        """
        dcg = 0.0
        for i in range(min(k, len(relevance_scores))):
            rel = relevance_scores[i]
            dcg += (2 ** rel - 1) / math.log2(i + 2)
        return dcg

    expected = dcg(relevance, k)/dcg(sorted(relevance, reverse=True), k)

    actual = solution.evaluate(test)

    assert(abs(expected - actual) < 0.01, f"""
            ❌ Тест не пройден: Сильное расхождение метрики NDCG
            Data: {test}
            Expected: {expected}
            Actual: {actual}
            """)
    

# === Тест recall@5 ===
def test_evaluate_recall_at_5(task_info,
                               k = 5):
    if task_info["metric"] != "recall@5":
        pytest.skip("Метрика в задании не recall@5")

    solution = load_solution_module()

    test = pd.DataFrame([
        {"movie_id": 250, "genres": 'Drama|Horror'},  # не релевантный
        {"movie_id": 251, "genres": 'Crime'},  # релевантный
        {"movie_id": 260, "genres": 'Action|Fantasy'},  # не релевантный
        {"movie_id": 266, "genres": 'Comedy|Romance|Crime'},  # релевантный
        {"movie_id": 280, "genres": 'Romance|Drama'}  # не релевантный
    ])
    solution.fit(test)
    relevant = {251, 266}

    expected = len(set(test["movie_id"].values) & set(relevant))/len(relevant)

    actual = solution.evaluate(test)

    assert isinstance(actual, float)
    assert abs(actual - expected) < 0.01, (f"""
            ❌ Тест не пройден: Сильное расхождение метрики recall@5
            Data: {test}
            Expected: {expected}
            Actual: {actual}
            """)
