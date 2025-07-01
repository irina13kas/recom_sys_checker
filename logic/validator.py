import subprocess
import sys
import os
import json
import tempfile
from typing import Dict

def run_pytest(task_info: Dict) -> str:
    """
    Запускает pytest с передачей task_info как параметра.
    Возвращает текстовый отчет.
    """
    test_file_map = {
        "collaborative": "logic/tests/collaborative_tests.py",
        "content_based": "logic/tests/content_based_tests.py"
    }

    test_file = test_file_map.get(task_info["type"])
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as temp_file:
        json.dump(task_info, temp_file)
        temp_path = temp_file.name

    try:
        # Запускаем pytest и получаем stdout/stderr
        result = subprocess.run(
            ["pytest", test_file, f"--task_info_path={temp_path}"],
            capture_output=True,
            text=True
        )
        #print(result)
        error_lines = [
            line[8:] if line.startswith("E       ") else line
            for line in result.stdout.splitlines() + result.stderr.splitlines()
            if line.strip().startswith("E")
        ]

        error_lines = [line.encode().decode('unicode_escape') for line in error_lines]

        if result.returncode != 0 and error_lines:
            return "❌ Тесты не пройдены. Подробности:\n" + "\n".join(error_lines)

        return "✅ Все тесты пройдены успешно!"
    finally:
        os.remove(temp_path)


def run_flake8(file_path="solutions/solution.py") -> str:
    print(f"🔍 Проверка стиля с помощью flake8 для файла: {file_path}...")
    result = subprocess.run(
        ["flake8", file_path, "--ignore=W293"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return "✅ flake8: Стиль кода соответствует стандарту.\n"
    else:
        return f"❌ flake8: Найдены проблемы со стилем:\n{result.stdout}"


def run_black_check(file_path="solutions/solution.py") -> str:
    print(f"🔍 Проверка форматирования с помощью black для файла: {file_path}...")
    result = subprocess.run(
        ["black", "--check", "--diff", file_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


    if result.returncode == 0:
        return "✅ black: Форматирование корректное.\n"
    else:
        return (
            "❌ black: Форматирование отличается от стандарта black.\n\n"
            "📋 Подробности:\n"
             f"uYTYT^ {result.stdout}"
        )


def generate_report(task_info: Dict) -> str:
    print("📋 Начинается проверка решения...\n")
    report = []

    # Проверка функциональности
    functional_report = run_pytest(task_info)
    functional_report_str = str(functional_report) if functional_report is not None else "Нет данных"
    report.append(f"🧪 Функциональные тесты\n{'-' * 30}\n{functional_report_str}")
    # Проверка стиля кода flake8
    flake8_report = run_flake8()
    report.append("🎨 Стиль кода (flake8)\n" + "-" * 30 + "\n" + flake8_report)

    # Проверка black
    black_report = run_black_check()
    report.append("🧱 Форматирование кода (black)\n" + "-" * 30 + "\n" + black_report)

    # Финальный вывод
    full_report = "\n\n".join(report)
    print("✅ Проверка завершена.\n")

    return full_report
