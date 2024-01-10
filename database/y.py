import sqlite3

connection = sqlite3.connect('produk.db')
cursor = connection.cursor()

# Tabel Peran (Role)
cursor.execute("INSERT INTO roles (role_name) VALUES ('Admin')")
cursor.execute("INSERT INTO roles (role_name) VALUES ('Customer')")

# Tabel Pengguna (User)
cursor.execute("INSERT INTO users (username, email, password, role_id) VALUES ('admin', 'admin@example.com', 'adminpass', 1)")
cursor.execute("INSERT INTO users (username, email, password, role_id) VALUES ('customer1', 'customer1@example.com', 'customerpass', 2)")

# Tabel Produk (Product)
cursor.execute("INSERT INTO tb_product (name, price, stock, photo, description) VALUES ('Product A', 50, 100, 'static/imgs/pexels-juan-pablo-serrano-arenas-1246437.jpg', 'Description for Product A')")
cursor.execute("INSERT INTO tb_product (name, price, stock, photo, description) VALUES ('Product B', 75, 50, 'static/imgs/f310nt-web.jpg', 'Description for Product B')")

# Tabel Pesanan (Order)
cursor.execute("INSERT INTO orders (customer_id, product_id, order_date, quantity, total_amount) VALUES (2, 1, '2024-01-06', 2, 100)")
cursor.execute("INSERT INTO orders (customer_id, product_id, order_date, quantity, total_amount) VALUES (2, 2, '2024-01-07', 1, 75)")

# Tabel Cart
cursor.execute("INSERT INTO cart (user_id, product_id, quantity, total_amount) VALUES (2, 1, 2, 100)")
cursor.execute("INSERT INTO cart (user_id, product_id, quantity, total_amount) VALUES (2, 2, 1, 75)")

connection.commit()
connection.close()
