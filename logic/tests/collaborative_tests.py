import pytest
import random
import pandas as pd
import numpy as np
import importlib.util
from pathlib import Path
from typing import List
from sklearn.metrics import mean_squared_error

# === Загрузка модуля ===
def load_solution_module():
    path = Path("solution.py")
    spec = importlib.util.spec_from_file_location("solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# === Расширенные данные ===
@pytest.fixture
def get_dummy_data():
    """
    Возвращает расширенный DataFrame для тестов user-based и item-based фильтрации.
    Колонки: user_id, item, rating
    """
    random.seed(42)
    users = list(range(1, 21))        # 20 пользователей
    items = list(range(100, 120))     # 20 предметов
    data = []

    # Каждый пользователь оценивает от 5 до 10 случайных предметов
    for user in users:
        rated_items = random.sample(items, k=random.randint(5, 10))
        for item in rated_items:
            rating = random.randint(1, 5)
            data.append((user, item, rating))

    df = pd.DataFrame(data, columns=['user_id', 'item', 'rating'])
    return df

dummy_data = get_dummy_data()

# === Тесты структуры ===
def test_has_required_functions():
    solution = load_solution_module()
    assert hasattr(solution, 'fit'), "Отсутствует функция fit"
    assert hasattr(solution, 'recommend'), "Отсутствует функция recommend"
    assert hasattr(solution, 'evaluate'), "Отсутствует функция evaluate"

def test_fit_runs_without_error(dummy_data):
    solution = load_solution_module()
    solution.fit(dummy_data)

def test_recommend_returns_k_items(dummy_data):
    solution = load_solution_module()
    solution.fit(dummy_data)
    recs = solution.recommend(user_id=1, k=2)
    assert isinstance(recs, list)
    assert all(isinstance(i, int) for i in recs)
    assert len(recs) == 2

def test_recommend_items_not_seen(dummy_data):
    solution = load_solution_module()
    solution.fit(dummy_data)
    seen_items = dummy_data[dummy_data['user_id'] == 1]['item'].tolist()
    recs = solution.recommend(user_id=1, k=2)
    assert not any(item in seen_items for item in recs), "Рекомендации включают просмотренные элементы"

def test_repeat_fit_stability(dummy_data):
    solution = load_solution_module()
    solution.fit(dummy_data)
    recs_1 = solution.recommend(1, 2)
    solution.fit(dummy_data)
    recs_2 = solution.recommend(1, 2)
    assert recs_1 == recs_2, "Рекомендации после повторного обучения должны совпадать"

# === Метрики ===

def test_rmse_calculation():
    y_true = [3, 4, 5]
    y_pred = [2.5, 4.5, 4.0]
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    expected = np.sqrt(((3 - 2.5) ** 2 + (4 - 4.5) ** 2 + (5 - 4) ** 2) / 3)
    assert round(rmse, 3) == round(expected, 3)

def precision_at_k(recommended: List[int], relevant: List[int], k: int) -> float:
    recommended_k = recommended[:k]
    hits = sum(1 for item in recommended_k if item in relevant)
    return hits / k

def test_precision_at_k():
    recs = [1, 2, 3, 4, 5]
    relevant = [3, 4, 7]
    score = precision_at_k(recs, relevant, 5)
    assert abs(score - 0.4) < 1e-6

# === Проверка evaluate на dummy_data ===

def test_evaluate_returns_correct_rmse(dummy_data):
    solution = load_solution_module()
    train = dummy_data.sample(frac=0.7, random_state=42)
    test = dummy_data.drop(train.index)
    solution.fit(train)

    # Вычисление ожидаемого RMSE (если используется как baseline)
    merged = pd.merge(test, train, on=["user_id", "item"], suffixes=("_test", "_train"))
    if not merged.empty:
        expected_rmse = np.sqrt(mean_squared_error(merged["rating_test"], merged["rating_train"]))
    else:
        expected_rmse = 0.0

    user_score = solution.evaluate(test)
    assert abs(user_score - expected_rmse) < 0.1, f"Ожидалось {expected_rmse}, получено {user_score}"
