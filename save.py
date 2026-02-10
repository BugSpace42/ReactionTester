import csv
import datetime
import os

def save_to_csv(results, filename="results.csv"):
    """Сохраняет результаты в CSV файл"""

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

    print(f"Данные сохранены в {filename}")
    return filename