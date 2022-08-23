from datetime import datetime


def write_execution_time(file_name: str, successful: bool, delta: float, datetime: datetime, destination: str):
    with open(file_name, "a") as bench_file:
        bench_file.write(f"{destination};{successful};{datetime.strftime('%H:%M:%S-%d.%m.%Y')};{delta:.2f}\n")
