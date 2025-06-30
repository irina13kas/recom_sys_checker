import pytest
import random
import os
import pandas as pd
import numpy as np
import importlib.util
from pathlib import Path
from typing import List
import json
from sklearn.metrics import mean_squared_error

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

    users = list(range(1, 21))
    items = list(range(100, 120))
    data = []

    for user in users:
        rated_items = random.sample(items, k=random.randint(5, 10))
        for item in rated_items:
            rating = random.randint(1, 5)
            data.append((user, item, rating))

    return pd.DataFrame(data, columns=['user_id', 'item', 'rating'])

# === Тесты структуры ===
def test_has_required_functions():
    solution = load_solution_module()
    assert hasattr(solution, 'fit'), "Отсутствует функция fit"
    assert hasattr(solution, 'recommend'), "Отсутствует функция recommend"
    assert hasattr(solution, 'evaluate'), "Отсутствует функция evaluate"

def test_fit_runs_without_error():
    sample_data = get_dummy_data()
    solution = load_solution_module()
    solution.fit(sample_data)

# === Тесты recommend и fit ===
@pytest.mark.parametrize("k", [1, 2, 3])
def test_fit_and_recommend_on_generated(task_info, k, generated_dataset):
    solution = load_solution_module()
    print(f"TASK_INFO: {task_info}")
    solution.fit(generated_dataset)
    user_id = generated_dataset["user_id"].iloc[0]
    recs = solution.recommend(user_id, k=k)
    assert isinstance(recs, list)
    assert len(recs) == k, f"""
        ❌ Тест не пройден:
        Входные данные: {generated_dataset}
        Ожидалось: {k}
        Получено: {len(recs)}
        """

    if task_info["filter_type"] == "user_based":
        # Допустим, проверим, что рекомендации разные для разных пользователей
        user_2 = generated_dataset["user_id"].iloc[1]
        recs_2 = solution.recommend(user_2, k=k)

        recs = list(map(int, recs))
        recs_2 = list(map(int, recs_2))
        if recs == recs_2:
            message = (
                f"\n❌ Рекомендации совпадают для двух разных пользователей при user-based фильтрации.\n"
                f"👤 user_id 1: {user_id} → recs: {recs}\n"
                f"👤 user_id 2: {user_2} → recs: {recs_2}\n"
                f"📎 Ожидалось: разные рекомендации для разных пользователей\n"
                f"📂 Данные:\n{generated_dataset[generated_dataset['user_id'].isin([user_id, user_2])]}"
            )
            raise AssertionError(message)
    elif task_info["filter_type"] == "item_based":
        # Проверим, что item'ы рекомендованы на основе похожих на просмотренные
        seen_items = generated_dataset[generated_dataset["user_id"] == user_id]["item"].tolist()
        assert not any(item in seen_items for item in recs), (f"""
            ❌ Тест не пройден: Item-based: не должны рекомендоваться уже просмотренные
            Входные данные: {generated_dataset}
            Ожидалось: {False}
            Получено: {True}
            """)
        
def test_recommend_items_not_seen(task_info, generated_dataset):
    solution = load_solution_module()

    solution.fit(generated_dataset)

    user_id = generated_dataset["user_id"].iloc[0]
    seen_items = set(generated_dataset[generated_dataset["user_id"] == user_id]["item"])
    recs = solution.recommend(user_id=user_id, k=3)

    assert isinstance(recs, list)
    if task_info["filter_type"] == "item_based":
        # В item-based обязаны быть только новые item'ы
        assert all(item not in seen_items for item in recs), (f"""
            ❌ Тест не пройден: Item-based: не должны рекомендоваться уже просмотренные
            Входные данные: {generated_dataset}
            Ожидалось: {False}
            Получено: {True}
            """)
    elif task_info["filter_type"] == "user_based":
        # В user-based иногда допускается, если не было ничего другого
        assert len(recs) > 0, (f"""
            ❌ Тест не пройден: 
            Входные данные: {generated_dataset}
            Ожидалось: {"Должны быть хоть какие-то элементы"}
            Получено: {"Список пустой"}
            """)

def test_repeat_fit_stability(task_info, generated_dataset):
    solution = load_solution_module()

    user_id = generated_dataset["user_id"].iloc[0]
    k = 3
    solution.fit(generated_dataset)
    recs_1 = solution.recommend(user_id, k)

    solution.fit(generated_dataset)
    recs_2 = solution.recommend(user_id, k)

    if task_info["filter_type"] == "user_based":
        assert recs_1 == recs_2, (f"""
            ❌ Тест не пройден: User-based: рекомендации после повторного fit должны совпадат
            Входные данные: {generated_dataset}
            Ожидалось: {"Совпадение рекомендаций"}
            Получено: {f"Выявлено расхождение. \nРекоммендации после 1-ого обучения: {recs_1} \nРекоммендации после 2-ого обучения: {recs_2}"}
            """)
    elif task_info["filter_type"] == "item_based":
        # Допускаем небольшую разницу — item-based может быть менее стабильной
        assert len(set(recs_1) & set(recs_2)) > 1, (f"""
            ❌ Тест не пройден: Item-based: слишком сильное расхождение рекомендаций
            Входные данные: {generated_dataset}
            Ожидалось: {"Совпадение рекомендаций"}
            Получено: {f"Выявлено сильное расхождение (более 1 элемента). \nРекоммендации после 1-ого обучения: {recs_1} \nРекоммендации после 2-ого обучения: {recs_2}"}
            """)
# === Метрики ===

# === Тест precision@2 ===
def test_evaluate_precision_at_2(task_info, generated_dataset):
    if task_info["metric"] != "precision@2":
        pytest.skip("Метрика в задании не precision@2")
    
    train = generated_dataset
    solution = load_solution_module()
    solution.fit(train)

    user_id = train["user_id"].iloc[0]
    k = 2

    test = pd.DataFrame([
        {"user_id": user_id, "item": 101, "rating": 5},  # релевантный
        {"user_id": user_id, "item": 100, "rating": 2},  # не релевантный
    ])

    recs = solution.recommend(user_id, k=k)
    print(f"Пользователь: {user_id}")
    print(f"Рекоммендации: {recs}")
    relevant_items = {100}
    hits = len(set(recs) & relevant_items)
    expected_precision = hits / k

    result = solution.evaluate(test)

    assert isinstance(result, float)
    assert abs(result - expected_precision) < 0.01, f"""
            ❌ Тест не пройден: Сильное расхождение метрики
            Входные данные: {generated_dataset}
            Ожидалось: {expected_precision}
            Получено: {result}
            """

# === Тест RMSE ===
def test_evaluate_returns_correct_rmse(task_info,generated_dataset):
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
        expected_rmse = np.sqrt(mean_squared_error(merged["rating_test"], merged["rating_train"]))
    else:
        expected_rmse = 0.0

    user_score = solution.evaluate(test)
    if user_score - expected_rmse <= 0.1:
        pytest.fail(f"""
    ❌ Тест не пройден: Сильное расхождение метрики
    Входные данные: {generated_dataset}
    Ожидалось: {expected_rmse}
    Получено: {user_score}
    """)

# === Тест recall@3 ===
def test_evaluate_recall_at_3(task_info, generated_dataset):
    if task_info["metric"] != "recall@3":
        pytest.skip("Метрика в задании не RMSE")

    train = generated_dataset
    solution = load_solution_module()
    solution.fit(train)

    user_id = train["user_id"].iloc[0]
    k = 3
    # Два релевантных item’а, из них один рекомендован — ожидаем recall 0.5
    test = pd.DataFrame([
        {"user_id": user_id, "item": 115, "rating": 4},
        {"user_id": user_id, "item": 116, "rating": 5},
        {"user_id": user_id, "item": 117, "rating": 2},  # не релевантный
    ])

    recs = solution.recommend(user_id, k=k)

    relevant = {115, 116}
    retrieved_relevant = len(set(recs) & relevant)
    expected_recall = retrieved_relevant / len(relevant)

    result = solution.evaluate(test)

    assert isinstance(result, float)
    assert abs(result - expected_recall) < 0.01, (f"""
            ❌ Тест не пройден: Сильное расхождение метрики
            Входные данные: {generated_dataset}
            Ожидалось: {expected_recall}
            Получено: {result}
            """)
