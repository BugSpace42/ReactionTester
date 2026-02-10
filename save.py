import csv
import datetime
import os
from typing import List
from excel_manager import save_to_excel

def save_to_csv(results: List[float], filename: str = "results.csv") -> str:
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                'Дата', 'Время', 'Тест №',
                'Время реакции (мс)', 'Среднее (мс)'
            ])

        timestamp = datetime.datetime.now()
        avg_time = sum(results) / len(results) if results else 0

        for i, time_ms in enumerate(results, 1):
            writer.writerow([
                timestamp.date(),
                timestamp.time(),
                i,
                f"{time_ms:.0f}",
                f"{avg_time:.0f}"
            ])

    print(f"Данные сохранены в CSV: {filename}")
    return filename


def save_data(results: List[float], tester_name: str = "Тестируемый",
              format_type: str = "excel") -> str:
    if not results:
        raise ValueError("Нет данных для сохранения")

    if format_type.lower() == "excel":
        return save_to_excel(results, tester_name)
    elif format_type.lower() == "csv":
        return save_to_csv(results)
    else:
        raise ValueError(f"Неизвестный формат: {format_type}")

save_to_file = save_data