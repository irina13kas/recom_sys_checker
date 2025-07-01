from logic.validator import generate_report
from logic.task_generator import TaskFactory
from report_csv import save_report_to_csv  # если используется

class TaskService:
    def __init__(self):
        self.task_info = None
        self.task_text = None
        self.solution_path = None

    def generate_task(self):
        self.task_text, self.task_info = TaskFactory.generate_description()
        return self.task_text, self.task_info

    def upload_solution(self, uploaded_file):
        # Сохраняем файл как solution.py
        with open("solutions/solution.py", "wb") as f:
            f.write(uploaded_file.read())
        self.solution_path = "solutions/solution.py"
        return self.solution_path

    def validate_solution(self):
        if not self.task_info or not self.solution_path:
            raise ValueError("Отсутствуют task_info или путь к решению")
        return generate_report(self.task_info)

    # def export_report(self, report: str, path: str = None) -> str:
    #     return save_report_to_csv(report, path)
