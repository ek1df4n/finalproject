import tkinter as tk
from tkinter import ttk
import sqlite3

# Инициализация SQLite базы данных
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                salary REAL
                )''')
conn.commit()

# Функция для добавления нового сотрудника
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    
    if name and salary:
        cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
                       (name, phone, email, salary))
        conn.commit()
        clear_entries()
        update_treeview()

# Функция для обновления информации о сотруднике
def update_employee():
    selected_item = treeview.selection()
    if selected_item:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = salary_entry.get()
        
        if name and salary:
            employee_id = treeview.item(selected_item, 'values')[0]
            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?",
                           (name, phone, email, salary, employee_id))
            conn.commit()
            clear_entries()
            update_treeview()

# Функция для удаления сотрудника
def delete_employee():
    selected_item = treeview.selection()
    if selected_item:
        employee_id = treeview.item(selected_item, 'values')[0]
        cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        conn.commit()
        clear_entries()
        update_treeview()

# Функция для поиска сотрудника по ФИО
def search_employee():
    search_name = search_entry.get()
    cursor.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + search_name + '%',))
    employees = cursor.fetchall()
    clear_treeview()
    for employee in employees:
        treeview.insert('', 'end', values=employee)

# Функция для очистки полей ввода
def clear_entries():
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    salary_entry.delete(0, 'end')

# Функция для очистки виджета Treeview
def clear_treeview():
    for item in treeview.get_children():
        treeview.delete(item)

# Функция для обновления виджета Treeview
def update_treeview():
    clear_treeview()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    for employee in employees:
        treeview.insert('', 'end', values=employee)

# Создание графического интерфейса
root = tk.Tk()
root.title("Список сотрудников компании")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Добавление полей для ввода информации о сотруднике
name_label = ttk.Label(frame, text="ФИО:")
name_label.grid(row=0, column=0, sticky='w')
name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = ttk.Label(frame, text="Номер телефона:")
phone_label.grid(row=1, column=0, sticky='w')
phone_entry = ttk.Entry(frame)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

email_label = ttk.Label(frame, text="Email:")
email_label.grid(row=2, column=0, sticky='w')
email_entry = ttk.Entry(frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

salary_label = ttk.Label(frame, text="Заработная плата:")
salary_label.grid(row=3, column=0, sticky='w')
salary_entry = ttk.Entry(frame)
salary_entry.grid(row=3, column=1, padx=5, pady=5)

# Кнопки для управления сотрудниками
add_button = ttk.Button(frame, text="Добавить", command=add_employee)
add_button.grid(row=4, column=0, padx=5, pady=5)

update_button = ttk.Button(frame, text="Изменить", command=update_employee)
update_button.grid(row=4, column=1, padx=5, pady=5)

delete_button = ttk.Button(frame, text="Удалить", command=delete_employee)
delete_button.grid(row=4, column=2, padx=5, pady=5)

# Поле для поиска сотрудника по ФИО
search_label = ttk.Label(frame, text="Поиск по ФИО:")
search_label.grid(row=5, column=0, sticky='w')
search_entry = ttk.Entry(frame)
search_entry.grid(row=5, column=1, padx=5, pady=5)

search_button = ttk.Button(frame, text="Найти", command=search_employee)
search_button.grid(row=5, column=2, padx=5, pady=5)

# Создание виджета Treeview для вывода данных
treeview = ttk.Treeview(frame, columns=('ID', 'ФИО', 'Телефон', 'Email', 'Зарплата'))
treeview.heading('ID', text='ID')
treeview.heading('ФИО', text='ФИО')
treeview.heading('Телефон', text='Телефон')
treeview.heading('Email', text='Email')
treeview.heading('Зарплата', text='Зарплата')
treeview.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Заполнение Treeview данными из базы
update_treeview()

# Запуск приложения
root.mainloop()

# Закрытие соединения с базой данных при выходе из приложения
conn.close()
 