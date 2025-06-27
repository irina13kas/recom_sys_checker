import subprocess
import json
import csv
from pathlib import Path
from task_generator import CollaborativeTaskGenerator

CSV_PATH = Path("validation_report.csv")
TESTS_DIR = Path("tests")


def write_csv_row(row):
    header = ["Тип", "Фильтрация", "Название", "Статус", "Сообщение"]
    write_header = not CSV_PATH.exists()
    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)


def generate_task_info():
    generator = CollaborativeTaskGenerator()
    task_text, task_info = generator.generate_task()

    # (опционально) сохраняем в файл
    with open("task_info.json", "w", encoding="utf-8") as f:
        json.dump(task_info, f, indent=2, ensure_ascii=False)

    print("📘 Сгенерировано задание:")
    print(task_text)
    return task_info


def check_style():
    print("⚙️ Проверка стиля...")
    flake8 = subprocess.run(["flake8", "solution.py"], capture_output=True, text=True)
    write_csv_row(["Style", "-", "flake8", "PASS" if flake8.returncode == 0 else "FAIL", flake8.stdout.strip() or "OK"])

    black = subprocess.run(["black", "--check", "solution.py"], capture_output=True, text=True)
    write_csv_row(["Style", "-", "black", "PASS" if black.returncode == 0 else "FAIL", black.stdout.strip() or "OK"])


def run_tests(filter_type):
    test_file = TESTS_DIR / f"test_{filter_type}.py"
    if not test_file.exists():
        write_csv_row(["Test", filter_type, "-", "FAIL", f"Файл {test_file.name} не найден"])
        return

    result = subprocess.run(
        ["pytest", str(test_file), "--json-report", "--json-report-file=report.json"],
        capture_output=True,
        text=True
    )

    if Path("report.json").exists():
        with open("report.json", encoding="utf-8") as f:
            report = json.load(f)

        for test in report.get("tests", []):
            name = test["nodeid"]
            status = test["outcome"]
            msg = "OK" if status == "passed" else test.get("call", {}).get("longrepr", "Ошибка")
            write_csv_row(["Test", filter_type, name, "PASS" if status == "passed" else "FAIL", str(msg).strip().replace("\n", " ")[:300]])


def main():
    if CSV_PATH.exists():
        CSV_PATH.unlink()

    task_info = generate_task_info()
    filter_type = task_info.get("filter_type", "user_based")

    check_style()
    run_tests(filter_type)

    print(f"\n✅ Отчёт сохранён: {CSV_PATH}")


if __name__ == "__main__":
    main()
