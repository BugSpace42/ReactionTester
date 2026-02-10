import tkinter as tk
from tkinter import ttk, messagebox
import threading

from save import *
from game import *

class MinimalApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тест реакции")
        self.window.geometry("400x300")

        self.results = []

        self.label = tk.Label(self.window, text="Тестирование реакции", font=("Arial", 14))
        self.label.pack(pady=20)

        self.start_button = tk.Button(
            self.window,
            text="Начать тест",
            command=self.start_test,
            height=2,
            width=20
        )
        self.start_button.pack(pady=10)

        self.save_button = tk.Button(
            self.window,
            text="Сохранить",
            command=self.save_results,
            state='disabled'
        )
        self.save_button.pack(pady=10)

        self.results_label = tk.Label(self.window, text="Результаты: --")
        self.results_label.pack(pady=20)

    def start_test(self):
        self.start_button.config(state='disabled')
        self.results_label.config(text="Запуск игры...")

        thread = threading.Thread(target=self.run_game)
        thread.daemon = True
        thread.start()

    def run_game(self):
        self.results = reaction_test()
        self.window.after(0, self.update_ui)

    def update_ui(self):
        if self.results:
            avg = sum(self.results) / len(self.results)
            self.results_label.config(
                text=f"Среднее: {avg:.0f} мс\n" +
                     f"Лучшее: {min(self.results):.0f} мс"
            )
            self.save_button.config(state='normal')

        self.start_button.config(state='normal')
        messagebox.showinfo("Готово", f"Тест завершен!\n{len(self.results)} попыток")

    def save_results(self):
        if self.results:
            filename = save_to_csv(self.results)
            messagebox.showinfo("Сохранено", f"Данные в {filename}")

    def run(self):
        self.window.mainloop()