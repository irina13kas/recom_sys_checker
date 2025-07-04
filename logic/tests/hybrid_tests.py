import pytest
import random
import os
import pandas as pd
import numpy as np
import importlib.util
from pathlib import Path
from sklearn.metrics import mean_squared_error

@pytest.fixture(params=[5, 10])
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
def get_dummy_data(seed=10):
    if seed is not None:
        random.seed(seed)
    else:
        seed = 10
    max_value = 120
    if(seed>10):
        max_value = seed/10 + 110
    brands = ['Adidas','H&M','Zara','Gucci','Nike']
    product_names = ['Dress','Shoes','Jeans','Sweater','T-shirt']
    users_id = [random.randint(30, 40) for _ in range(seed)]
    products_id = [random.randint(110, max_value) for _ in range(seed)]
    data = []

    for i in range(seed):
        user_id = random.choice(users_id)
        product_id = random.choice(products_id)
        product_name = random.choice(product_names)
        brand = random.choice(brands)
        price = random.randint(10, 50)
        rating = random.randrange(100,501)/100
        data.append({
            'user_id': user_id,
            'product_id': product_id,
            'product_name': product_name,
            'brand': brand,
            'price': price,
            'rating': rating
            })

    return pd.DataFrame(data)

# === Тесты структуры ===
def test_has_required_functions():
    solution = load_solution_module()
    assert hasattr(solution, 'fit'), "There is no fit"
    assert hasattr(solution, 'recommend'), "There is no recommend"
    assert hasattr(solution, 'evaluate'), "There is no evaluate"

def test_fit_runs_without_error():
    sample_data = get_dummy_data()
    solution = load_solution_module()
    solution.fit(sample_data)

# === Тесты recommend и fit ===
import pytest

@pytest.mark.parametrize("k", [1, 2, 3])
def test_fit_and_recommend_on_generated(k, generated_dataset):
    solution = load_solution_module()

    solution.fit(generated_dataset)
    print(generated_dataset)
    user_id = generated_dataset["user_id"].iloc[0]
    print(f"size: {user_id}")
    all_product_ids = set(generated_dataset["product_id"].values)

    recs = solution.recommend(user_id, k=k)
    assert len(recs) != 0, f"""
        Тест не пройден:
        Data: {generated_dataset}
        Expected: Должен быть рекомендован хотя бы один фильм
        Actual: 0
        """
    assert isinstance(recs, list), f"""
        Тест не пройден:
        Expected: type list
        Actual: {type(recs)}
        """

    assert len(recs) <= k, f"""
        Тест не пройден:
        Expected: {k} recommendations
        Actual: {len(recs)}
        """

    assert len(set(recs)) == len(recs), f"""
        Тест не пройден:
        Recommendations should be unique
        Actual: {recs}
        """

    assert all(pid in all_product_ids for pid in recs), f"""
        Тест не пройден:
        Some product_ids from the recommendations are missing from the dataset
        Expected: {all_product_ids}
        Actual: {recs}
        """
def test_repeat_fit_stability( generated_dataset):
    solution = load_solution_module()
    solution.fit(generated_dataset)
    user_id = generated_dataset["user_id"].iloc[0]
    k = 3
    solution.fit(generated_dataset)
    recs_1 = solution.recommend(user_id, k)

    solution.fit(generated_dataset)
    recs_2 = solution.recommend(user_id, k)

    assert sorted(recs_1) == sorted(recs_2), (f"""
        Тест не пройден: User-based: рекомендации после повторного fit должны совпадат
        Data: {generated_dataset}
        Expected: {"Совпадение рекомендаций"}
        Actual: {f"Выявлено расхождение."
                f"Рекоммендации после 1-ого обучения: {recs_1}"
                f"Рекоммендации после 2-ого обучения: {recs_2}"}
        """)
# === Метрики ===

# === Тест precision@5 ===
def test_evaluate_precision_at_5(task_info,
                                  k=5):
    if task_info["metric"] != "precision@5":
        pytest.skip("Метрика в задании не precision@5")
    
    solution = load_solution_module()

    test = pd.DataFrame([
        {'user_id':1, 'product_id': 117,'product_name':'Dress','brand':'Gucci','price':16,'rating':2.34}, # не релевантный
        {'user_id':1, 'product_id': 111,'product_name':'Shoes','brand':'Adidas','price':12,'rating':3.56}, # не релевантный
        {'user_id':2, 'product_id': 112,'product_name':'T-shirt','brand':'Nike','price':5,'rating':4.00}, # не релевантный
        {'user_id':3, 'product_id': 110,'product_name':'Dress','brand':'Gucci','price':16,'rating':5.00}, # релевантный
        {'user_id':3, 'product_id': 112,'product_name':'T-shirt','brand':'Nike','price':5,'rating':3.88}, # не релевантный
        {'user_id':3, 'product_id': 114,'product_name':'Jeans','brand':'Adidas','price':8,'rating':3.44}, # не релевантный
        {'user_id':2, 'product_id': 110,'product_name':'Dress','brand':'Gucci','price':16,'rating':4.12}, # релевантный
        {'user_id':4, 'product_id': 115,'product_name':'Sweater','brand':'H&M','price':10,'rating':3.30}, # не релевантный
    ])
    solution.fit(test)
    recs = [110,114]
    relevant_items = set(
        test[(test["rating"] >= 4) & (test["brand"] == "Gucci")]["product_id"]
    )

    hits = len(set(recs) & relevant_items)
    print(len(relevant_items))
    expected = hits / k

    result = solution.evaluate(test)
    print(result)
    assert isinstance(result, float)
    assert abs(result - expected) < 0.1, f"""
        Тест не пройден: Сильное расхождение метрики precision@5
        Data: {test}
        Relevant objects: {relevant_items}
        Recommendations: {recs}
        Expected: {expected}
        Actual: {result}
        """

# === Тест RMSE ===
def test_evaluate_returns_correct_rmse(task_info):
    if task_info["metric"] != "RMSE":
        pytest.skip("Метрика в задании не RMSE")
    
    solution = load_solution_module()
    dummy_data = get_dummy_data(1000)
    train = dummy_data.sample(frac=0.7, random_state=42)
    test = dummy_data.drop(train.index)
    solution.fit(train)

    merged = pd.merge(test, train, on=["user_id", "product_id"], suffixes=("_test", "_train"))
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
    

# === Тест recall@5 ===
def test_evaluate_recall_at_5(task_info,
                               k = 5):
    if task_info["metric"] != "recall@5":
        pytest.skip("Метрика в задании не recall@5")

    solution = load_solution_module()

    test = pd.DataFrame([
        {'user_id':1, 'product_id': 117,'product_name':'Dress','brand':'Gucci','price':16,'rating':2.34}, # не релевантный
        {'user_id':1, 'product_id': 111,'product_name':'Shoes','brand':'Adidas','price':12,'rating':3.56}, # не релевантный
        {'user_id':2, 'product_id': 112,'product_name':'T-shirt','brand':'Nike','price':5,'rating':4.00}, # не релевантный
        {'user_id':3, 'product_id': 110,'product_name':'Dress','brand':'Gucci','price':16,'rating':5.00}, # релевантный
        {'user_id':3, 'product_id': 112,'product_name':'T-shirt','brand':'Nike','price':5,'rating':3.88}, # не релевантный
        {'user_id':3, 'product_id': 114,'product_name':'Jeans','brand':'Adidas','price':8,'rating':3.44}, # не релевантный
        {'user_id':2, 'product_id': 110,'product_name':'Dress','brand':'Gucci','price':16,'rating':4.12}, # релевантный
        {'user_id':4, 'product_id': 115,'product_name':'Sweater','brand':'H&M','price':10,'rating':3.30}, # не релевантный
    ])
    solution.fit(test)
    relevant = set(
        test[(test["rating"] >= 4) & (test["brand"] == "Gucci")]["product_id"][:k]
    )
    recs = [110,114]
    expected = len(set(recs) & set(relevant))/len(relevant)

    actual = solution.evaluate(test)

    assert isinstance(actual, float)
    assert abs(actual - expected) < 0.1, (f"""
            Тест не пройден: Сильное расхождение метрики recall@5
            Входные данные: {test}
            Expected: {expected}
            Actual: {actual}
            """)
