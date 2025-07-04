import pytest
import json

def pytest_addoption(parser):
    parser.addoption("--task_info_path", action="store")

@pytest.fixture
def task_info(request):
    path = request.config.getoption("--task_info_path")
    if path is not None:
        with open(path, "r") as f:
            return json.load(f)