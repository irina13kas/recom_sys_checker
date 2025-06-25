import random

def generate():
    algo = random.choice(["TF-IDF", "count-based", "cosine similarity"])
    metric = random.choice(["precision@5","recall@5","MAE","NDCG"])
    dataset = random.choice(["movie_content.csv", "video_game_content.csv"])

    task_text = (
        f"Тип задачи: Контентная рекомендательная система\n\n"
        f"📘 Описание:\n"
        f"Реализуйте контентную систему рекомендаций, используя метод {algo}. "
        f"На вход подаётся описание объектов (например, фильмов) и взаимодействия пользователей с ними.\n\n"
        f"🎯 Рассчитайте метрику **{metric}** для качества рекомендаций.\n\n"
        f"📎 Датасет: {dataset}"
    )

    task_info = {
        "type": "content",
        "algorithm": algo,
        "metric": metric,
        "dataset": dataset
    }

    return task_text, task_info