import sqlite3

def create_connection():
    conn = sqlite3.connect('store.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        login TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        fio TEXT NOT NULL,
                        phone_number TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS workers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        login TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        fio TEXT NOT NULL,
                        post TEXT NOT NULL,
                        phone_number TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        manufacturer TEXT NOT NULL,
                        price REAL NOT NULL,
                        quantity_in_stock INTEGER NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        manufacturer TEXT NOT NULL,
                        price REAL NOT NULL,
                        payment_method TEXT,
                        FOREIGN KEY (client_id) REFERENCES clients(id))''')

    conn.commit()
    conn.close()


def register_client(fio, phone_number, email, login, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (fio, phone_number, email, login, password) VALUES (?, ?, ?, ?, ?)",
                   (fio, phone_number, email, login, password))
    conn.commit()
    conn.close()


def register_worker(fio, post, phone_number, email, login, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workers (fio, post, phone_number, email, login, password) VALUES (?, ?, ?, ?, ?, ?)",
                   (fio, post, phone_number, email, login, password))
    conn.commit()
    conn.close()

def get_clients():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_products():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def get_orders():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return orders

def add_product(name, category, description, manufacturer, price, quantity_in_stock):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, description, manufacturer, price, quantity_in_stock) VALUES (?, ?, ?, ?, ?, ?)",
        (name, category, description, manufacturer, price, quantity_in_stock))
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def place_order(client_id, product_id, payment_method):
    conn = create_connection()
    cursor = conn.cursor()

    # Получаем информацию о товаре
    cursor.execute("SELECT name, category, description, manufacturer, price, quantity_in_stock FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product:
        # Проверяем, достаточно ли товара в наличии
        if product[5] > 0:  # product[5] - это quantity_in_stock
            # Перемещаем товар в таблицу заказов
            cursor.execute(
                "INSERT INTO orders (client_id, name, category, description, manufacturer, price, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (client_id, product[0], product[1], product[2], product[3], product[4], payment_method)
            )
            # Уменьшаем количество товара на 1
            cursor.execute("UPDATE products SET quantity_in_stock = quantity_in_stock - 1 WHERE id = ?", (product_id,))
            conn.commit()
        else:
            print("Товар недоступен в достаточном количестве.")
    else:
        print("Товар не найден.")

    conn.close()

def get_orders_by_client(client_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE client_id = ?", (client_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

create_tables()