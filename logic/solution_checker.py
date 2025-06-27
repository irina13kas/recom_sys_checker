import subprocess

def check_solution(filepath):
    print("🔍 Проверка функциональности через pytest:")
    subprocess.run(["pytest", filepath])

    print("\n🎯 Проверка code style через flake8:")
    subprocess.run(["flake8", filepath])

    print("\n🧹 Проверка форматирования через black:")
    subprocess.run(["black", "--check", filepath])