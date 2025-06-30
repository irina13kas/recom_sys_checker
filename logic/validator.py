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

    #     output = result.stdout + "\n" + result.stderr

    #     # Если тесты упали — ищем сообщение от assert
    #     if result.returncode != 0:
    #         # Ищем строки, начинающиеся с "❌" или содержащие AssertionError
    #         for line in output.splitlines():
    #             if "❌ Тест не пройден" in line:
    #                 return line + "\n"  # первая строка
    #         # если не нашли — вернём общее сообщение
    #         return "❌ Тесты не пройдены. Подробности:\n" + output

    #     return "✅ Все тесты пройдены успешно!"
    # finally:
    #     os.remove(temp_path)



# def extract_failure_details(full_output: str, test_name: str) -> str:
#     """
#     Улучшенная версия функции извлечения сообщений об ошибках.
#     Корректно обрабатывает параметризованные тесты и многострочные сообщения.
#     """
#     lines = full_output.splitlines()
#     collecting = False
#     error_lines = []
#     test_header = f"{test_name} FAILED"
    
#     for line in lines:
#         # Находим начало ошибки для конкретного теста
#         if test_header in line:
#             collecting = True
#             continue
        
#         # Если находим следующий тест или конец блока - прекращаем сбор
#         if collecting and ("====" in line or "FAILED" in line or "PASSED" in line or "logic/tests/" in line):
#             break
        
#         # Собираем строки ошибки
#         if collecting and line.strip():
#             # Очищаем строки от технических префиксов pytest
#             clean_line = line.replace("E   ", "").strip()
#             if not clean_line.startswith((">", "_", "FAILED", "PASSED")):
#                 error_lines.append(clean_line)
    
#     # Если нашли стандартное сообщение AssertionError, извлекаем его
#     if error_lines:
#         for i, line in enumerate(error_lines):
#             if "AssertionError:" in line:
#                 # Берем все строки после AssertionError
#                 return "\n".join(error_lines[i:])
        
#         # Если AssertionError нет, возвращаем все собранные строки
#         return "\n".join(error_lines)
    
#     # Альтернативный метод поиска для случаев, когда ошибка в другом формате
#     for i, line in enumerate(lines):
#         if test_header in line:
#             # Ищем следующую непустую строку после FAILED
#             for next_line in lines[i+1:]:
#                 if next_line.strip() and not next_line.startswith(("_", ">", "E", "FAILED", "PASSED")):
#                     return next_line.strip()
    
#     return "Тест не пройден (детали не указаны)"

# def run_pytest(task_info: Dict) -> str:
#     """
#     Запускает pytest с передачей task_info как параметра.
#     Возвращает текстовый отчет.
#     """
#     test_file_map = {
#         "collaborative": "logic/tests/collaborative_tests.py",
#     }

#     test_file = test_file_map.get(task_info["type"])
#     if not test_file or not os.path.exists(test_file):
#         return f"[Ошибка] Не найден тестовый файл для типа задачи: {task_info['type']}"

#     # Передаем task_info через переменную окружения
#     env = os.environ.copy()
#     env["TASK_INFO"] = json.dumps(task_info)

#     print(f"🔍 Запуск pytest для файла: {test_file}...")

#     result = subprocess.run(
#         [
#             sys.executable,
#             "-m", "pytest",
#             test_file,
#             "-v",
#             "--no-header",
#             "--no-summary",
#             "--tb=native",  # Более чистое отображение ошибок
#         ],
#         text=True,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         env=env,
#         encoding="utf-8",
#         errors="replace",
#     )
#     output = result.stdout + "\n" + result.stderr
#     report_lines = []
    
#     # Собираем информацию о всех тестах
#     test_results = []
#     for line in output.splitlines():
#         if "logic/tests/" in line and ("PASSED" in line or "FAILED" in line):
#             parts = line.split("::")
#             test_name = parts[1].split()[0]
#             status = "PASSED" if "PASSED" in line else "FAILED"
#             test_results.append((test_name, status, line))
    
#     # Обрабатываем каждый тест
#     for test_name, status, raw_line in test_results:
#         if status == "FAILED":
#             error_msg = extract_failure_details(output, test_name)
            
#             # Дополнительная очистка сообщения
#             if "AssertionError:" in error_msg:
#                 error_msg = error_msg.split("AssertionError:")[1].strip()
            
#             report_lines.append(f"❌ Тест не пройден: {test_name}")
#             report_lines.append(f"   Ошибка: {error_msg}")
#             report_lines.append("")  # Пустая строка для разделения
#         else:
#             report_lines.append(f"✅ Тест пройден: {test_name}")

#     return "\n".join(report_lines)

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
