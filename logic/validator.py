import subprocess
import sys
import os
import json
from typing import Dict


def run_pytest(task_info: Dict) -> str:
    """
    Запускает pytest с передачей task_info как параметра.
    Возвращает текстовый отчет.
    """
    test_file_map = {
        "collaborative": "logic/tests/collaborative_tests.py",
        # Здесь можно расширить под другие типы заданий
    }

    test_file = test_file_map.get(task_info["type"])
    if not test_file or not os.path.exists(test_file):
        return f"[Ошибка] Не найден тестовый файл для типа задачи: {task_info['type']}"

    # Сохраняем task_info во временный файл, чтобы pytest мог его загрузить

    task_info_str = json.dumps(task_info)

    env = os.environ.copy()
    env["TASK_INFO"] = task_info_str  # передаём как переменную окружения

    print(f"🔍 Запуск pytest для файла: {test_file}...")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-v", "-rA"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    output = result.stdout

    report_lines = []
    #print("STDOUT:\n", result.stdout)

    
    for line in output.splitlines():
        if "PASSED" in line:
            test_name = line.split("::")[-1].split()[0]
            report_lines.append(f"✅ PASSED: {test_name}")
        elif "FAILED" in line:
            test_name = line.split("::")[-1].split()[0]
            report_lines.append(f"❌ FAILED: {test_name}")
            
            # Добавляем сообщение об ошибке из следующих строк
            error_message = extract_error_message(output, line)
            print(f"ERROR: {error_message}")
            if error_message:
                report_lines.append(f"    Сообщение: {error_message}")
            
            in_error = True

    return "\n".join(report_lines or ["✅ Все тесты пройдены успешно!"])

def extract_error_message(full_output, failed_line):
    """Извлекает сообщение об ошибке после строки с FAILED"""
    lines = full_output.splitlines()
    idx = lines.index(failed_line)
    
    # Ищем следующие строки с ошибкой
    for i in range(idx+1, min(idx+100, len(lines))):  # Проверяем 10 следующих строк
        print(f"!!!!! {lines[i]}")
        if "assert:" in lines[i]:
            return lines[i].split("assert:")[1].strip()
        if "assert       " in lines[i]:  # Строки с ошибкой в pytest
            return lines[i][8:].strip()
    
    return None

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
