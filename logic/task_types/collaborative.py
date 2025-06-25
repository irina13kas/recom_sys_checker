import random 

def generate():
    filter_type = random.choice(["user_based","item_based"])
    algo = random.choice(["SVD","ALS","k-NN"])
    metric = random.choice(["precision@5","recall@5","RMSE","NDCG"])
    similarity = random.choice(["cosine", "pearson"])
    k = random.choice([5, 10, 20])
    dataset = random.choice(["movie_ratings.csv","games_collaborative.csv"])

    task_text = (
        f"Тип задачи: Коллаборативная фильтрация ({filter_type})\n\n"
        f"📘 Описание:\n"
        f"Реализуйте функцию предсказания оценок пользователей на основе {filter_type} фильтрации "
        f"с использованием алгоритма {algo}.\n\n"
        f"📌 Параметры:\n"
        f"- Количество соседей: k = {k}\n"
        f"- Метрика схожести: {similarity}\n\n"
        f"🎯 Оцените результат с помощью метрики **{metric}**.\n\n"
        f"📎 Датасет: {dataset}"
    )

    task_info = {
        "type": "collaborative",
        "filter_type": filter_type,
        "algorithm": algo,
        "metric": metric,
        "similarity": similarity,
        "k": k,
        "dataset": dataset
    }

    return task_text, task_info