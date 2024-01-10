import sqlite3

connection = sqlite3.connect('produk.db')
cursor = connection.cursor()

# Tabel Peran (Role)
cursor.execute('''
CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL
);
''')

# Tabel Pengguna (User)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
''')

# Tabel Produk (Product)
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_product (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    price INTEGER,
    stock INTEGER,
    photo BLOB NOT NULL,
    description VARCHAR(500)
);
''')

# Tabel Pesanan (Order)
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount REAL,
    -- Ganti 'role_id' menjadi 'customer_id' dalam foreign key
    FOREIGN KEY (customer_id) REFERENCES users(user_id)
);
''')

connection.commit()
connection.close()
