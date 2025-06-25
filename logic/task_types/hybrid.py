import random 

def generate():
    cf_part = random.choice(["SVD", "ALS"])
    cb_part = random.choice(["TF-IDF", "count-based"])
    metric = random.choice(["precision@5","recall@5","RMSE"])
    dataset = random.choice(["hybrid_movies.csv", "hybrid_books.csv"])

    task_text = (
        f"Тип задачи: Гибридная рекомендательная система\n\n"
        f"📘 Описание:\n"
        f"Реализуйте гибридную рекомендательную систему, совмещающую методы:\n"
        f"- Коллаборативная часть: {cf_part}\n"
        f"- Контентная часть: {cb_part}\n\n"
        f"📂 Данные:\n"
        f"- `user_id`, `item_id`, `rating`, `description`, `title`\n\n"
        f"🎯 Оцените результат с помощью метрики **{metric}**.\n\n"
        f"📎 Датасет: {dataset}"
    )

    task_info = {
        "type": "hybrid",
        "cf_algorithm": cf_part,
        "cb_algorithm": cb_part,
        "metric": metric,
        "dataset": dataset
    }

    return task_text, task_info