import subprocess
import shutil
import json
import tempfile

def run_pytest_on_collaborative_tests():
    task_info = {
        "filter_type": "user_based",
        "metric": "RSME"
    }
    test_file = 'logic/tests/collaborative_tests.py'
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as temp_file:
        json.dump(task_info, temp_file)
        temp_path = temp_file.name
    result = subprocess.run(
        ["pytest", test_file,  f"--task_info_path={temp_path}", "-q", "--tb=short"],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout + result.stderr

def test_collaborative_tests_run_on_correct_code():

    shutil.copy("tests/solutions/collaborative/solution_correct.py", "solutions/solution.py")

    exit_code, output = run_pytest_on_collaborative_tests()
    assert exit_code == 0, f"Тесты в collaborative_tests.py упали на корректном коде:\n{output}"

def test_collaborative_tests_fail_on_broken_code():

    shutil.copy("tests/solutions/collaborative/solution_broken.py", "solutions/solution.py")

    exit_code, output = run_pytest_on_collaborative_tests()
    print(f"ТЕСТЫ УПАЛИ НА СЛОМАННОМ КОДЕ: {output}")
    assert exit_code != 0, "Тесты не упали на сломанном коде, хотя должны"

if __name__ == "__main__":
    for test_func in [test_collaborative_tests_run_on_correct_code, test_collaborative_tests_fail_on_broken_code]:
        try:
            test_func()
            print(f"{test_func.__name__}: PASS")
        except AssertionError as e:
            print(f"{test_func.__name__}: FAIL\n{e}")
