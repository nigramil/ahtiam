import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []

        # Ввод полей
        self.create_widgets()

    def create_widgets(self):
        # Дата
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        # Температура
        tk.Label(self.root, text="Температура (°C):").grid(row=1, column=0)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1)

        # Описание погоды
        tk.Label(self.root, text="Описание:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1)

        # Осадки
        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Осадки", variable=self.rain_var).grid(row=3, column=1)

        # Кнопки
        tk.Button(self.root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, pady=5)
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_to_json).grid(row=4, column=1)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_from_json).grid(row=4, column=2)

        # Таблица для отображения
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Температура", "Описание", "Осадки"), show='headings')
        for col in ("Дата", "Температура", "Описание", "Осадки"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=5, column=0, columnspan=3, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0)
        self.filter_date_entry = tk.Entry(self.root)
        self.filter_date_entry.grid(row=6, column=1)
        tk.Button(self.root, text="Применить", command=self.filter_by_date).grid(row=6, column=2)

        tk.Label(self.root, text="Фильтр по температуре выше:").grid(row=7, column=0)
        self.filter_temp_entry = tk.Entry(self.root)
        self.filter_temp_entry.grid(row=7, column=1)
        tk.Button(self.root, text="Применить", command=self.filter_by_temp).grid(row=7, column=2)

        tk.Button(self.root, text="Сброс фильтра", command=self.reset_filter).grid(row=8, column=1)

    def add_record(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc = self.desc_entry.get()

        # Проверка
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты")
            return

        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        if not desc:
            messagebox.showerror("Ошибка", "Описание не должно быть пустым")
            return

        rain = self.rain_var.get()

        record = {
            "date": date_str,
            "temperature": temp,
            "description": desc,
            "rain": rain
        }

        self.records.append(record)
        self.update_tree()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.rain_var.set(False)

    def update_tree(self, filtered_records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = filtered_records if filtered_records is not None else self.records
        for rec in data:
            self.tree.insert("", "end", values=(
                rec["date"], rec["temperature"], rec["description"], "Да" if rec["rain"] else "Нет"
            ))

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            with open(filename, "w") as f:
                json.dump(self.records, f, indent=4)
            messagebox.showinfo("Сохранено", "Данные сохранены в файл")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r") as f:
                self.records = json.load(f)
            self.update_tree()

    def filter_by_date(self):
        date_str = self.filter_date_entry.get()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты")
            return
        filtered = [rec for rec in self.records if rec["date"] == date_str]
        self.update_tree(filtered)

    def filter_by_temp(self):
        try:
            temp_threshold = float(self.filter_temp_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число")
            return
        filtered = [rec for rec in self.records if rec["temperature"] > temp_threshold]
        self.update_tree(filtered)

    def reset_filter(self):
        self.update_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
