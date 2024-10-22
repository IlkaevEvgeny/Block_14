import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()

# Создание таблицы Users, если она не существует
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        balance INTEGER NOT NULL
    )
""")

# Заполнение таблицы 10-ю записями.
for i in range(10):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (f"User{i+1}", f"example{i+1}@gmail.com", (i+1)*10, 1000))

# Выборка всех записей, проверка заполнения.
cursor.execute("SELECT * FROM Users")
users = cursor.fetchall()
print("Перевоначальная таблица.")
for user in users:
    print(user)
print(" ")

# Обновление balance на 500 у каждой второй записи, начиная с первой
cursor.execute("UPDATE Users SET balance = 500 WHERE id % 2 = 1")

# Выборка всех записей, проверка заполнения.
cursor.execute("SELECT * FROM Users")
users = cursor.fetchall()
print("Пользователи с обновленным балансом.")
for user in users:
    print(user)
print(" ")

# Удаление каждой третьей записи, начиная с первой
cursor.execute("DELETE FROM Users WHERE id % 3 = 1")

# Выборка всех записей, проверка заполнения.
cursor.execute("SELECT * FROM Users")
users = cursor.fetchall()
print("Удален каждый третий.")
for user in users:
    print(user)
print(" ")

# Выборка всех записей, где возраст не равен 60
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
users = cursor.fetchall()

# Выборка всех записей, проверка заполнения.
print("Те кому не 60.")
for user in users:
    print(user)
print(" ")

'''
# Удалим всех для следующего запуска
cursor.execute("DELETE FROM Users")
'''

# Сохраним и закроем
conn.commit()
conn.close()