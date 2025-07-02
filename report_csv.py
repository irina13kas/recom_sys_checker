import os
import csv
from datetime import datetime

def save_report_to_csv(report_text: str, path: str = None):
    os.makedirs("reports", exist_ok=True)

    if path is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"reports/report_{timestamp}.csv"

    with open(path, mode="w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["message"])
        for line in report_text.strip().split("\n"):
            writer.writerow([line])

    return path