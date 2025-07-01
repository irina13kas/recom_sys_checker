import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from controller import TaskService
import os

if 'service' not in st.session_state:
    st.session_state.service = TaskService()

service = st.session_state.service

# Стилизация
st.set_page_config(page_title="Рекомендательная система", layout="centered")

# 1. Генерация задания
st.title("🎯 Генератор задания по рекомендательной системе")

if "task_info" not in st.session_state:
    st.session_state.task_info = None
if "task_text" not in st.session_state:
    st.session_state.task_text = ""
if "uploaded_solution_path" not in st.session_state:
    st.session_state.uploaded_solution_path = ""

if st.button("🔄 Сгенерировать задание"):
    task_text, task_info = service.generate_task()
    st.session_state.task_text = task_text
    st.session_state.task_info = task_info
    service.task_info = st.session_state.task_info
    service.task_text = st.session_state.task_text

# 2. Вывод задания
if st.session_state.task_text:
    st.markdown("### 📝 Задание")
    st.markdown(st.session_state.task_text)
    
    with open("template/solution.py", "rb") as f:
        template_bytes = f.read()

    st.download_button(
        label="📥 Скачать шаблон solution.py",
        data=template_bytes,
        file_name="solution.py",
        mime="text/x-python"
    )

    dataset_path = "logic/datasets/" + st.session_state.task_info["dataset"]
    # Проверяем что файл существует
    if os.path.exists(dataset_path):
        with open(dataset_path, "rb") as f:
            data = f.read()
        st.download_button(
            label="Скачать датасет",
            data=data,
            file_name=os.path.basename(dataset_path),
            mime="text/csv"
        )
    else:
        st.error("Файл датасета не найден!")


# 3. Загрузка файла
if st.session_state.task_info:
    st.markdown("---")
    st.markdown("### 📎 Прикрепите свой `solution.py`")

    uploaded_file = st.file_uploader("Загрузите файл solution.py", type=["py"])

    if uploaded_file:
        
        # Можно сохранить файл в сессию или временно на диск
        # Пример - сохраняем во временный файл:
        save_path = os.path.join("solutions/", uploaded_file.name)
        os.makedirs("solutions", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        service.upload_solution(uploaded_file)

        st.session_state.uploaded_solution_path = save_path
        st.success(f"Файл {uploaded_file.name} загружен!")


# 4. Кнопка проверки и 5. Отчет
if st.session_state.uploaded_solution_path:
    if st.button("🚀 Проверить решение"):
        report = service.validate_solution()
        csv_path = service.export_report(report)

        st.session_state.report_text = report
        st.session_state.report_csv_path = csv_path

        st.markdown("### 📊 Отчет по решению")
        st.code(report, language="markdown")

        # if st.session_state.get("report_csv_path"):
        #     with open(st.session_state.report_csv_path, "rb") as f:
        #         st.download_button(
        #             label="📥 Скачать отчет (.csv)",
        #             data=f.read(),
        #             file_name=Path(st.session_state.report_csv_path).name,
        #             mime="text/csv"
        #         )