import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))
# === Интерфейс ===

class ValidatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Проверка рекомендательной системы")
        self.root.geometry("1000x800")

        self.solution_loaded = False

        # Кнопка: Сгенерировать задание
        self.task_btn = tk.Button(root, text="📘 Сгенерировать задание", command=self.generate_task)
        self.task_btn.pack(pady=10)

        # Текст задания
        self.task_text = scrolledtext.ScrolledText(root, height=12, wrap=tk.WORD)
        self.task_text.pack(padx=10, fill=tk.BOTH)
        self.task_text.insert(tk.END, "Задание появится здесь...")
        self.task_text.config(state=tk.DISABLED)

        # Кнопка загрузки решения
        self.upload_btn = tk.Button(root, text="📂 Загрузить файл solution.py", command=self.upload_solution)
        self.upload_btn.pack(pady=10)

        # Кнопка проверки (отключена до загрузки)
        self.validate_btn = tk.Button(root, text="✅ Проверить решение", state=tk.DISABLED, command=self.run_validator)
        self.validate_btn.pack(pady=5)

        # Отчёт
        self.report_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
        self.report_text.pack(padx=10, pady=10, fill=tk.BOTH)
        self.report_text.insert(tk.END, "Здесь будет показан результат проверки...")
        self.report_text.config(state=tk.DISABLED)

        # Сохранить отчёт
        self.save_btn = tk.Button(root, text="💾 Скачать отчёт CSV", state=tk.DISABLED, command=self.save_report)
        self.save_btn.pack(pady=10)

    def generate_task(self):
        from logic.task_types.collaborative import CollaborativeTaskGenerator

        generator = CollaborativeTaskGenerator()
        task_text, task_info = generator.generate_task()

        with open("task_info.json", "w", encoding="utf-8") as f:
            import json
            json.dump(task_info, f, indent=2, ensure_ascii=False)

        self.task_text.config(state=tk.NORMAL)
        self.task_text.delete("1.0", tk.END)
        self.task_text.insert(tk.END, task_text.strip())
        self.task_text.config(state=tk.DISABLED)
        
        dataset_file = Path("logic/datasets/collaborative") / task_info["dataset"]
        print(dataset_file)
        if dataset_file.exists():
            if hasattr(self, "dataset_link"):
                self.dataset_link.config(
                    text=f"📁 Открыть датасет: {dataset_file.name}",
                    fg="blue",
                    cursor="hand2"
                )
                self.dataset_link.bind("<Button-1>", lambda e: webbrowser.open(dataset_file.resolve().as_uri()))
            else:
                self.dataset_link = tk.Label(self.root, text=f"📁 Открыть датасет: {dataset_file.name}",
                                            fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
                self.dataset_link.pack(pady=5)
                self.dataset_link.bind("<Button-1>", lambda e: webbrowser.open(dataset_file.resolve().as_uri()))
        else:
            if hasattr(self, "dataset_link"):
                self.dataset_link.config(text="❌ Датасет не найден", fg="red", cursor="arrow")
            else:
                self.dataset_link = tk.Label(self.root, text="❌ Датасет не найден", fg="red")
                self.dataset_link.pack(pady=5)
            
        messagebox.showinfo("✅ Успешно", "Задание сгенерировано.")

    def upload_solution(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python file", "*.py")])
        if file_path:
            try:
                shutil.copy(file_path, "solution.py")
                self.solution_loaded = True
                self.validate_btn.config(state=tk.NORMAL)
                messagebox.showinfo("✅ Загружено", "Файл solution.py загружен.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def run_validator(self):
        self.report_text.config(state=tk.NORMAL)
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, "🔄 Проверка запущена...\n")
        self.report_text.update()

        result = subprocess.run(["python", "logic/validator.py"], capture_output=True, text=True)
        if result.returncode == 0:
            self.report_text.insert(tk.END, "\n✅ Проверка завершена успешно.\n\n")
        else:
            self.report_text.insert(tk.END, "\n❌ Проверка завершена с ошибками.\n\n")
            self.report_text.insert(tk.END, result.stderr)

        # Вывод содержимого .csv
        csv_path = Path("validation_report.csv")
        if csv_path.exists():
            with open(csv_path, encoding="utf-8") as f:
                self.report_text.insert(tk.END, f.read())
                self.save_btn.config(state=tk.NORMAL)
        else:
            self.report_text.insert(tk.END, "⚠️ Отчёт не найден.")

        self.report_text.config(state=tk.DISABLED)

    def save_report(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
        if file:
            try:
                shutil.copy("validation_report.csv", file)
                messagebox.showinfo("✅ Сохранено", "Отчёт успешно сохранён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить отчёт:\n{e}")


# === Запуск ===
if __name__ == "__main__":
    root = tk.Tk()
    app = ValidatorGUI(root)
    root.mainloop()
