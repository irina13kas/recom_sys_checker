import pytest
import random
import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_squared_error

def generated_dataset():
    return get_dummy_data(1000)

# === Расширенные данные ===
def get_dummy_data(seed=10):
    if seed is not None:
        random.seed(seed)
    else:
        seed = 10

    brands = ['Adidas','H&M','Zara','Gucci','Nike']
    product_names = ['Dress','Shoes','Jeans','Sweater','T-shirt']
    users_id = [random.randint(30, 40) for _ in range(seed)]
    products_id = [random.randint(110, 120) for _ in range(seed)]
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

def evaluate(generated_dataset):
    print(generated_dataset)
    dummy_data = generated_dataset
    train = dummy_data.sample(frac=0.7, random_state=42)
    test = dummy_data.drop(train.index)
    print(train)
    merged = pd.merge(test, train, on=["user_id", "product_id"], suffixes=("_test", "_train"))
    print(merged)
    if len(merged)!=0:
        expected = np.sqrt(mean_squared_error(merged["rating_test"], merged["rating_train"]))
    else:
        expected = 0.0
    print(expected)

f = generated_dataset()
evaluate(f)