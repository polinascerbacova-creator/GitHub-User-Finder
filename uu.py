import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Создаём главное окно
window = tk.Tk()
window.title("GitHub User Finder")
window.geometry("500x400")

# Файл для сохранения избранных пользователей
FAVORITES_FILE = "favorites.json"

# Загружаем избранных пользователей из файла (если есть)
if os.path.exists(FAVORITES_FILE):
    with open(FAVORITES_FILE, "r") as f:
        favorites = json.load(f)
else:
    favorites = {}


# Функция поиска пользователя
def search_user():
    # Получаем текст из поля ввода
    username = entry.get().strip()

    # Проверяем, что поле не пустое
    if not username:
        messagebox.showerror("Ошибка", "Введите имя пользователя!")
        return

    try:
        # Отправляем запрос к GitHub API
        response = requests.get(f"https://api.github.com/users/{username}")

        if response.status_code == 200:
            # Если пользователь найден, получаем данные
            user_data = response.json()

            # Показываем данные в окне результатов
            result_text.delete(1.0, tk.END)  # Очищаем предыдущее содержимое
            result_text.insert(tk.END, f"Имя: {user_data.get('name', 'Не указано')}\n")
            result_text.insert(tk.END, f"Логин: {user_data.get('login', 'Не указано')}\n")
            result_text.insert(tk.END, f"Местоположение: {user_data.get('location', 'Не указано')}\n")
        else:
            messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Проблема с интернетом: {e}")


# Функция добавления в избранное
def add_to_favorites():
    username = entry.get().strip()
    if not username:
        messagebox.showwarning("Внимание", "Сначала найдите пользователя!")
        return

    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            user_data = response.json()
            # Добавляем в словарь избранных
            favorites[username] = {
                "name": user_data.get("name", "Не указано"),
                "location": user_data.get("location", "Не указано")
            }
            # Сохраняем в файл
            with open(FAVORITES_FILE, "w") as f:
                json.dump(favorites, f, indent=2)
            messagebox.showinfo("Успех", f"{username} добавлен в избранное!")
        else:
            messagebox.showerror("Ошибка", "Сначала найдите пользователя!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")


# Создаём элементы интерфейса
tk.Label(window, text="Введите имя пользователя GitHub:").pack(pady=5)

entry = tk.Entry(window, width=30)
entry.pack(pady=5)

tk.Button(window, text="Найти", command=search_user).pack(pady=5)
tk.Button(window, text="Добавить в избранное", command=add_to_favorites).pack(pady=5)

# Окно для показа результатов поиска
tk.Label(window, text="Результаты поиска:").pack(pady=(10, 0))
result_text = tk.Text(window, height=8, width=50)
result_text.pack(pady=5, padx=10)

# Окно для показа избранных пользователей
tk.Label(window, text="Избранные пользователи:").pack(pady=(10, 0))
favorites_text = tk.Text(window, height=6, width=50)
favorites_text.pack(pady=5, padx=10)


# Функция для обновления списка избранных
def update_favorites_list():
    favorites_text.delete(1.0, tk.END)
    for username, data in favorites.items():
        favorites_text.insert(tk.END, f"{username} - {data['name']} ({data['location']})\n")


# Сразу показываем текущие избранные
update_favorites_list()

# Запускаем приложение
window.mainloop()