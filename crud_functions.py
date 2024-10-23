import sqlite3

def initiate_db():

  # Подключение к базе данных
  conn = sqlite3.connect('mydatabase.db')
  cursor = conn.cursor()

  # Создание таблицы Products, если она не существует
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
      id INTEGER PRIMARY KEY,
      title TEXT NOT NULL,
      description TEXT,
      price INTEGER NOT NULL
    )
  """)
  conn.commit()
  conn.close()


# Возвращает все записи из таблицы Products.

def get_all_products():
  
  conn = sqlite3.connect('mydatabase.db')
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM Products")
  products = cursor.fetchall()

  conn.close()
  return products


