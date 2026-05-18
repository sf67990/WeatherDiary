import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from datetime import datetime

records = []

def add_record():
    date_str = entry_date.get()
    temperature_str = entry_temperature.get()
    description = entry_description.get()
    precipitation = var_precipitation.get()

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите правильную дату в формате ГГГГ-ММ-ДД")
        return

    try:
        temperature = float(temperature_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числовое значение температуры")
        return

    record = {
        "date": date_str,
        "temperature": temperature,
        "description": description,
        "precipitation": precipitation
    }

    records.append(record)
    update_table()
    clear_entries()

def clear_entries():
    entry_date.delete(0, tk.END)
    entry_temperature.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    var_precipitation.set(0)

def update_table(filtered_records=None):
    for row in tree.get_children():
        tree.delete(row)
    data = filtered_records if filtered_records is not None else records
    for rec in data:
        tree.insert('', tk.END, values=(
            rec["date"],
            rec["temperature"],
            rec["description"],
            "Да" if rec["precipitation"] else "Нет"
        ))

def filter_by_date():
    date_filter = entry_filter_date.get()
    if not date_filter:
        update_table()
        return
    filtered = [rec for rec in records if rec["date"] == date_filter]
    update_table(filtered)

def filter_by_temperature():
    temp_str = entry_filter_temperature.get()
    if not temp_str:
        update_table()
        return
    try:
        temp_filter = float(temp_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числовое значение температуры для фильтра")
        return
    filtered = [rec for rec in records if rec["temperature"] == temp_filter]
    update_table(filtered)

def reset_filters():
    entry_filter_date.delete(0, tk.END)
    entry_filter_temperature.delete(0, tk.END)
    update_table()

def save_to_json():
    filename = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON files", "*.json")])
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные успешно сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

def load_from_json():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filename:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                global records
                records = json.load(f)
            update_table()
            messagebox.showinfo("Успех", "Данные успешно загружены")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

root = tk.Tk()
root.title("Дневник погоды")
root.geometry("800x600")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Температура:").grid(row=0, column=2, padx=5, pady=5)
entry_temperature = tk.Entry(frame_input)
entry_temperature.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_input, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
entry_description = tk.Entry(frame_input, width=50)
entry_description.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

var_precipitation = tk.IntVar()
checkbox_precipitation = tk.Checkbutton(root, text="Осадки", variable=var_precipitation)
checkbox_precipitation.pack()

btn_add = tk.Button(root, text="Добавить запись", command=add_record)
btn_add.pack(pady=10)


columns = ("date", "temperature", "description", "precipitation")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())

tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


frame_filters = tk.Frame(root)
frame_filters.pack(pady=10)

tk.Label(frame_filters, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5)
entry_filter_date = tk.Entry(frame_filters)
entry_filter_date.grid(row=0, column=1, padx=5)

tk.Label(frame_filters, text="Фильтр по температуре:").grid(row=0, column=2, padx=5)
entry_filter_temperature = tk.Entry(frame_filters)
entry_filter_temperature.grid(row=0, column=3, padx=5)

btn_filter_date = tk.Button(frame_filters, text="Фильтр по дате", command=filter_by_date)
btn_filter_date.grid(row=0, column=4, padx=5)

btn_filter_temp = tk.Button(frame_filters, text="Фильтр по температуре", command=filter_by_temperature)
btn_filter_temp.grid(row=0, column=5, padx=5)

btn_reset = tk.Button(frame_filters, text="Сбросить фильтры", command=reset_filters)
btn_reset.grid(row=0, column=6, padx=5)

frame_menu = tk.Frame(root)
frame_menu.pack(pady=10)

btn_save = tk.Button(frame_menu, text="Сохранить в JSON", command=save_to_json)
btn_save.pack(side=tk.LEFT, padx=10)

btn_load = tk.Button(frame_menu, text="Загрузить из JSON", command=load_from_json)
btn_load.pack(side=tk.LEFT, padx=10)

root.mainloop()