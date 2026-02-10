import tkinter as tk
from tkinter import ttk, messagebox
import threading
from tkinter import filedialog
from save import *
from game import *


class MinimalApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тест реакции")
        self.window.geometry("450x400")

        self.results = []
        self.tester_name = tk.StringVar(value="Тестируемый")
        self.save_format = tk.StringVar(value="excel")

        self.label = tk.Label(self.window, text="Тестирование реакции", font=("Arial", 14))
        self.label.pack(pady=20)

        name_frame = tk.Frame(self.window)
        name_frame.pack(pady=5)

        tk.Label(name_frame, text="Имя:").pack(side=tk.LEFT, padx=5)
        tk.Entry(name_frame, textvariable=self.tester_name, width=20).pack(side=tk.LEFT, padx=5)

        format_frame = tk.Frame(self.window)
        format_frame.pack(pady=5)

        tk.Label(format_frame, text="Формат:").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(format_frame, text="Excel", variable=self.save_format,
                       value="excel").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(format_frame, text="CSV", variable=self.save_format,
                       value="csv").pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(
            self.window,
            text="Начать тест (3 попытки)",
            command=self.start_test,
            height=2,
            width=25,
            bg="#4CAF50",  # Зеленый цвет
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.start_button.pack(pady=15)

        self.progress = ttk.Progressbar(
            self.window,
            length=300,
            mode='indeterminate'
        )
        self.progress.pack(pady=10)

        self.save_button = tk.Button(
            self.window,
            text="💾 Сохранить результаты",
            command=self.save_results,
            state='disabled',
            height=1,
            width=20,
            bg="#2196F3",  # Синий цвет
            fg="white"
        )
        self.save_button.pack(pady=10)

        # Метка для результатов
        self.results_label = tk.Label(
            self.window,
            text="Результаты появятся здесь",
            font=("Arial", 10),
            wraplength=400,
            justify="left"
        )
        self.results_label.pack(pady=20)

        # Статусная строка
        self.status_label = tk.Label(
            self.window,
            text="Готов к тестированию",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def start_test(self):
        self.start_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.results_label.config(text="Тестирование...\nЖдите появления зеленого экрана")
        self.status_label.config(text="Тестирование запущено...")
        self.progress.start(10)

        # Запускаем в отдельном потоке
        thread = threading.Thread(target=self.run_game)
        thread.daemon = True
        thread.start()

    def run_game(self):
        """Запускает игру и собирает данные"""
        try:
            self.results = reaction_test()
            self.window.after(0, self.update_ui)
        except Exception as e:
            self.window.after(0, lambda: self.show_error(str(e)))

    def update_ui(self):
        """Обновление интерфейса после теста"""
        self.progress.stop()

        if self.results:
            # Форматируем результаты
            result_text = "РЕЗУЛЬТАТЫ:\n\n"

            successful = [r for r in self.results if r > 0]
            errors = len([r for r in self.results if r <= 0])

            for i, res in enumerate(self.results, 1):
                if res > 0:
                    result_text += f"• Тест {i}: {res:.0f} мс\n"
                elif res == -1:
                    result_text += f"• Тест {i}: Таймаут\n"
                else:
                    result_text += f"• Тест {i}: Ошибка\n"

            # Статистика
            result_text += f"\nСТАТИСТИКА:\n"
            result_text += f"Успешных: {len(successful)} из {len(self.results)}\n"

            if successful:
                avg = sum(successful) / len(successful)
                result_text += f"Среднее: {avg:.0f} мс\n"
                result_text += f"Лучшее: {min(successful):.0f} мс\n"
                result_text += f"Худшее: {max(successful):.0f} мс"

            self.results_label.config(text=result_text)
            self.save_button.config(state='normal')
            self.status_label.config(text=f"Тест завершен. Успешных: {len(successful)}/{len(self.results)}")
        else:
            self.results_label.config(text="Тест был прерван")
            self.status_label.config(text="Тест прерван")

        self.start_button.config(state='normal')

        if self.results:
            messagebox.showinfo(
                "Готово",
                f"Тестирование завершено!\n\n"
                f"Попыток: {len(self.results)}\n"
                f"Успешных: {len([r for r in self.results if r > 0])}\n"
                f"Нажмите 'Сохранить' для записи в файл."
            )

    def save_results(self):
        if not self.results:
            messagebox.showwarning("Нет данных", "Сначала проведите тестирование")
            return

        try:
            name = self.tester_name.get().strip()
            if not name:
                name = "Тестируемый"

            format_type = self.save_format.get()

            filename = save_to_file(
                results=self.results,
                tester_name=name,
                format_type=format_type
            )
            format_name = "Excel" if format_type == "excel" else "CSV"
            message = (f"Данные успешно сохранены!\n\n"
                       f"Файл: {filename}\n"
                       f"Формат: {format_name}\n"
                       f"Тестируемый: {name}\n"
                       f"Тестов: {len(self.results)}")

            if format_type == "excel":
                response = messagebox.askyesno(
                    "Сохранено",
                    message + "\n\nХотите открыть файл?",
                    icon='info'
                )
                if response:
                    import os
                    os.startfile(filename)  # Открываем файл
            else:
                messagebox.showinfo("Сохранено", message)

            self.status_label.config(text=f"Данные сохранены в {filename}")

        except Exception as e:
            self.show_error(f"Ошибка при сохранении: {str(e)}")

    def show_error(self, message):
        self.progress.stop()
        self.start_button.config(state='normal')
        self.status_label.config(text="Ошибка!")
        messagebox.showerror("Ошибка", message)

    def run(self):
        self.window.mainloop()