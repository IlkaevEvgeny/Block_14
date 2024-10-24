import sqlite3

# Создание таблиц Products и Users в базе данных,
#   если они еще не существуют.
def initiate_db():

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000 
        )
    """)

    conn.commit()
    conn.close()

def get_all_products():

  conn = sqlite3.connect('mydatabase.db')
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM Products")
  products = cursor.fetchall()

  conn.close()
  return products

# Добавление нового пользователя в таблицу Users.
def add_user(username, email, age):

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Users (username, email, age)
        VALUES (?, ?, ?)
    """, (username, email, age))

    conn.commit()
    conn.close()

# Проверка, существует ли пользователь с указанным username.
def is_included(username):

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM Users WHERE username = ?
    """, (username,))

    result = cursor.fetchone()
    conn.close()
    return bool(result)


