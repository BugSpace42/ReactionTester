from game import *
from save import *

def main():
    print("Тест на реакцию")

    # Запускаем тест
    data = reaction_test()

    if data:
        # Сохраняем результаты
        filename = save_to_csv(data)

        # Простая статистика
        print("\nСтатистика:")
        print(f"Количество тестов: {len(data)}")
        print(f"Лучшее время: {min(data):.0f} мс")
        print(f"Худшее время: {max(data):.0f} мс")
        print(f"Среднее время: {sum(data) / len(data):.0f} мс")
        print(f"\nДанные сохранены в: {filename}")

if __name__ == "__main__":
    main()