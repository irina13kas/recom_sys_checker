import pytest
import random
import os
import pandas as pd
import numpy as np
import importlib.util
from pathlib import Path
import subprocess
from sklearn.metrics import mean_squared_error

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
def get_dummy_data(task_info, seed=None):
    if seed is not None:
        random.seed(seed)

    users = list(range(1, 21))
    items = list(range(100, 200))
    data = []
    if(task_info["filter_type"]=="item_based"):
        for user in users:
            rated_items = random.sample(items, k=random.randint(1, 5))
            for item in rated_items:
                rating = random.randint(1, 5)
                data.append((user, item, rating))
    else:
        for item in items:
            rated_users = random.sample(users, k=random.randint(3, 5))
            for user in rated_users:
                rating = random.randint(1, 5)
                data.append((user, item, rating))

    return pd.DataFrame(data, columns=['user_id', 'item', 'rating'])

# === Тесты структуры ===
def test_has_required_functions():
    solution = load_solution_module()
    assert hasattr(solution, 'fit'), "There is no fit"
    assert hasattr(solution, 'recommend'), "There is no recommend"
    assert hasattr(solution, 'evaluate'), "There is evaluate"

def test_fit_runs_without_error(task_info):
    sample_data = get_dummy_data(task_info=task_info,seed=50)
    solution = load_solution_module()
    solution.fit(sample_data)

# === Тесты recommend и fit ===
@pytest.mark.parametrize("k", [1, 2, 3])
@pytest.mark.parametrize("seed", [5, 10, 50, 100])
def test_fit_and_recommend_on_generated(task_info,
                                         k, seed):
    generated_dataset = get_dummy_data(seed=seed, task_info=task_info)
    solution = load_solution_module()

    solution.fit(generated_dataset)
    user_id = generated_dataset["user_id"].iloc[0]
    recs = solution.recommend(user_id, k=k)
    assert isinstance(recs, list)
    # assert len(recs) != 0, f"""
    #     Тест не пройден:
    #     Data: {generated_dataset}
    #     Expected: Должен быть рекомендован хотя бы один фильм
    #     Actual: 0
    #     """
    assert len(recs)== k, f"""
        Тест не пройден:
        Data: {generated_dataset}
        Expected: {k}
        Actual: {len(recs)}
        """

    if task_info["filter_type"] == "user_based":
        user_2 = generated_dataset["user_id"].iloc[1]
        recs_2 = solution.recommend(user_2, k=k)

        recs = list(map(int, recs))
        recs_2 = list(map(int, recs_2))
        assert sorted(recs) != sorted(recs_2), (f"""
                Рекомендации совпадают для двух разных пользователей при user-based фильтрации."
                user_id 1: {user_id}  recs: {recs}"
                user_id 2: {user_2}  recs: {recs_2}"
                Expected: разные рекомендации для разных пользователей"
                Data:{generated_dataset}"
            """)
    elif task_info["filter_type"] == "item_based":
        seen_items = generated_dataset[generated_dataset["user_id"] == user_id]["item"].tolist()
        assert not any(item in seen_items for item in recs), (f"""
            Тест не пройден: Item-based: не должны рекомендоваться уже просмотренные
            Data: {generated_dataset}
            Expected: {False}
            Actual: {True}
            """)
        
@pytest.mark.parametrize("seed", [5, 10, 50, 100])     
def test_recommend_items_not_seen(task_info, 
                                  seed):
    solution = load_solution_module()
    generated_dataset = get_dummy_data(seed=seed, task_info=task_info)
    solution.fit(generated_dataset)

    user_id = generated_dataset["user_id"].iloc[0]
    seen_items = set(generated_dataset[generated_dataset["user_id"] == user_id]["item"])
    recs = solution.recommend(user_id=user_id, k=3)

    assert isinstance(recs, list)
    if task_info["filter_type"] == "item_based":
        # В item-based обязаны быть только новые item'ы
        assert all(item not in seen_items for item in recs), (f"""
            Тест не пройден: Item-based: не должны рекомендоваться уже просмотренные
            Data: {generated_dataset}
            Expected: {False}
            Actual: {True}
            """)
    elif task_info["filter_type"] == "user_based":
        # В user-based иногда допускается, если не было ничего другого
        assert len(recs) > 0, (f"""
            Тест не пройден: 
            Data: {generated_dataset}
            Expected: {"Должны быть хоть какие-то элементы"}
            Actual: {"Список пустой"}
            """)
@pytest.mark.parametrize("seed", [5, 10, 50, 100])
def test_repeat_fit_stability(task_info, 
                              seed):
    solution = load_solution_module()
    generated_dataset = get_dummy_data(seed=seed, task_info=task_info)
    solution.fit(generated_dataset)
    user_id = generated_dataset["user_id"].iloc[0]
    k = 3
    solution.fit(generated_dataset)
    recs_1 = solution.recommend(user_id, k)

    solution.fit(generated_dataset)
    recs_2 = solution.recommend(user_id, k)

    if task_info["filter_type"] == "user_based":
        assert sorted(recs_1) == sorted(recs_2), (f"""
            Тест не пройден: User-based: рекомендации после повторного fit должны совпадат
            Data: {generated_dataset}
            Expected: {"Совпадение рекомендаций"}
            Actual: {f"Выявлено расхождение."
                    f"Рекоммендации после 1-ого обучения: {recs_1}"
                    f"Рекоммендации после 2-ого обучения: {recs_2}"}
            """)
    elif task_info["filter_type"] == "item_based":
        # Допускаем небольшую разницу — item-based может быть менее стабильной
        assert len(set(recs_1) & set(recs_2)) > 1, (f"""
            Тест не пройден: Item-based: слишком сильное расхождение рекомендаций
            Data: {generated_dataset}
            Expected: {"Совпадение рекомендаций"}
            Actual: {f"Выявлено сильное расхождение (более 1 элемента)."
                     f"Рекоммендации после 1-ого обучения: {recs_1}"
                     f"Рекоммендации после 2-ого обучения: {recs_2}"}
            """)
# === Метрики ===

# === Тест precision@2 ===
def test_evaluate_precision_at_2(task_info,
                                  k=2):
    if task_info["metric"] != "precision@2":
        pytest.skip("Метрика в задании не precision@2")
    
    solution = load_solution_module()

    test = pd.DataFrame([
        {"user_id": 12, "item": 101, "rating": 5},  # релевантный
        {"user_id": 13, "item": 119, "rating": 2},  # не релевантный
        {"user_id": 13, "item": 120, "rating": 3},  # не релевантный
        {"user_id": 14, "item": 101, "rating": 4}, # релевантный
        {"user_id": 14, "item": 118, "rating": 4}, # релевантный
        {"user_id": 12, "item": 119, "rating": 3},  # не релевантный
    ])
    users_recs = [118, 120]
    items_recs = [118]
    relevant_items = [101, 118]
    if task_info['filter_types']=='user_based':
        expected = len(set(users_recs) & relevant_items)/k
    else:
        expected = len(set(items_recs) & relevant_items)/k
    actual = solution.evaluate(test)

    assert isinstance(actual, float)
    assert abs(actual - expected) < 0.1, f"""
            Тест не пройден: Сильное расхождение метрики precision@2
            Data: {test}
            Expected: {expected}
            Actual: {actual}
            """

# === Тест RMSE ===
def test_evaluate_returns_correct_rmse(task_info, 
                                       ):
    generated_dataset = get_dummy_data(seed=3, task_info=task_info)
    if task_info["metric"] != "RMSE":
        pytest.skip("Метрика в задании не RMSE")
    
    solution = load_solution_module()
    dummy_data = generated_dataset
    train = dummy_data.sample(frac=0.7, random_state=42)
    test = dummy_data.drop(train.index)
    solution.fit(train)

    # Вычисление ожидаемого RMSE (если используется как baseline)
    merged = pd.merge(test, train, on=["user_id", "item"], suffixes=("_test", "_train"))
    if not merged.empty:
        expected = np.sqrt(mean_squared_error(merged["rating_test"], merged["rating_train"]))
    else:
        expected = 0.0

    actual = solution.evaluate(test)
    assert abs(actual-expected) < 0.1, f"""
    Тест не пройден: Сильное расхождение метрики RMSE
    Data: {generated_dataset}
    Expected: {expected}
    Actual: {actual}
    """

# === Тест recall@3 ===
def test_evaluate_recall_at_3(task_info,
                               k = 3):
    if task_info["metric"] != "recall@3":
        pytest.skip("Метрика в задании не recall@3")

    solution = load_solution_module()

    test = pd.DataFrame([
        {"user_id": 12, "item": 115, "rating": 4}, # релевантный
        {"user_id": 12, "item": 116, "rating": 5}, # релевантный
        {"user_id": 13, "item": 117, "rating": 2},  # не релевантный
        {"user_id": 14, "item": 115, "rating": 4}, # релевантный
        {"user_id": 14, "item": 118, "rating": 4}, # релевантный
        {"user_id": 12, "item": 119, "rating": 3},  # не релевантный
    ])
    solution.fit(test)
    relevant = [115, 116, 118]
    users_recs = [118, 119]
    items_recs = [116, 118, 119]
    if task_info['filter_types']=='user_based':
        expected = len(set(users_recs) & set(relevant))/len(relevant)
    else:
        expected = len(set(items_recs) & set(relevant))/len(relevant)
    actual = solution.evaluate(test)
    assert isinstance(actual, float)
    assert abs(actual - expected) < 0.1, (f"""
            Тест не пройден: Сильное расхождение метрики recall@3
            Data: {test}
            Expected: {expected}
            Actual: {actual}
            """)
