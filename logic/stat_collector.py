import csv

def log_result(task_info, result_info, filename="results.csv"):
    headers = list(task_info.keys()) + list(result_info.keys())

    try:
        with open(filename, mode="x", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerow({**task_info, **result_info})

    except:
        with open(filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerow({**task_info, **result_info})