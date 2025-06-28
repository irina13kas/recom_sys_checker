import os
import csv
from datetime import datetime

def save_report_to_csv(report_text: str, path: str = None):
    # Создание директории, если её нет
    os.makedirs("reports", exist_ok=True)

    # Если путь не задан — используем с меткой времени
    if path is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"reports/report_{timestamp}.csv"

    # Сохраняем как CSV с одной колонкой: "message"
    with open(path, mode="w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["message"])  # Заголовок
        for line in report_text.strip().split("\n"):
            writer.writerow([line])

    return path  # Возвращаем путь к файлу
