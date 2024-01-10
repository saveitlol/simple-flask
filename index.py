from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os 
import re
from datetime import datetime
import sqlite3
import hashlib
import datetime

app = Flask('__name__')
app.config['SECRET_KEY'] = '!@#$%'
app.config['SESSION_TYPE'] = 'filesystem'

def connect_db():
    # app.secret_key = ''
    return sqlite3.connect("produk.db")
   

@app.route('/')
def index():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tb_product")
    products = cursor.fetchall()
    connection.close()
    return render_template('index.html', products=products)

@app.route('/lakslregister', methods =['GET', 'POST'])
def amslregister():
    msg = ''
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form and 'inpUsername' in request.form and 'inpAlamat' in request.form and 'inpNotelp' in request.form:

        email = request.form['inpEmail']
        passw = request.form['inpPass']
        username = request.form['inpUsername']
        alamat = request.form['inpAlamat']
        notelp = request.form['inpNotelp']
        connection = connect_db()

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not passw or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute("INSERT INTO useme (username,email,password,alamat,notelp)VALUES (%s,%s,%s,%s,%s)", (username, email, passw, alamat, notelp))  
            connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
     msg = ''
     if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
          email = request.form['inpEmail']
          passw = request.form['inpPass']
          connection = connect_db()
          cursor = connection.cursor()
          cursor.execute("SELECT * FROM users WHERE email = ? AND password = ? ", (email, passw,  ))
          result =cursor.fetchone()
          if result:
               session['is_logged_in'] = True
               session['username'] = result[1]
               session['user_id'] = result[0]
               return redirect(url_for('index'))
          else:
               msg = 'Incorrect username / password !'
               return render_template('login.html', msg = msg)
     else:
          msg='salah woe'
          return render_template('login.html')
     
@app.route('/guest')
def guest():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tb_product")
    products = cursor.fetchall()
    connection.close()
    return render_template('guest.html', products=products)

@app.route('/admin')
def read():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tb_product")
    products = cursor.fetchall()
    connection.close()
    return render_template('readmin.html', products=products)

@app.route('/post', methods=["POST"])
def create():
    connection = connect_db()
    cursor = connection.cursor()
    file = request.files['file']
    if file:
        # Save the uploaded file to the uploads folder
        filename = os.path.join('static/imgs', file.filename)
        file.save(filename)
    else:
        filename = None
    cursor.execute("INSERT INTO tb_product (name, price, stock, description,photo) VALUES (?, ?, ?, ?, ?)",
                   (request.form['nama'], request.form['harga'], request.form['stock'], request.form['deskripsi'],filename))
    connection.commit()
    connection.close()
    return redirect('/admin')

@app.route('/reupdate/<int:id>', methods=['GET'])
def get(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE id=?", (id,))
    post = cursor.fetchone()
    connection.close()
    return render_template('reupdate.html', post=post)

@app.route('/view_product/<int:id>', methods=['GET'])
def view_product(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE id=?", (id,))
    post = cursor.fetchone()
    connection.close()
    return render_template('view.html', post=post)

@app.route('/guest_view/<int:id>', methods=['GET'])
def guest_view(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tb_product WHERE id=?", (id,))
    post = cursor.fetchone()
    connection.close()
    return render_template('guest_view.html', post=post)

@app.route('/reupdate/<int:id>', methods=['POST'])
def update(id):
    connection = connect_db()
    cursor = connection.cursor()
    file = request.files['file']
    if file:
        # Save the uploaded file to the uploads folder
        filename = os.path.join('static/imgs', file.filename)
        file.save(filename)
    else:
        filename = None
    cursor.execute("UPDATE tb_product SET name=?, price=?, stock=?, description=? ,photo=? WHERE id=?",
                   (request.form['nama'], request.form['harga'], request.form['stok'], request.form['deskripsi'],filename, id))
    connection.commit()
    connection.close()
    return redirect('/admin')

@app.route('/delete/<int:id>')
def delete(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tb_product WHERE id=?", (id,))
    connection.commit()
    connection.close()
    return redirect('/admin')

@app.route('/addcart/<int:product_id>')
def cart(product_id):
    connection = connect_db()
    cursor = connection.cursor()
    
    queryProduct =cursor.execute("SELECT * FROM tb_product WHERE id=?", (product_id,))
    produk = queryProduct.fetchone()

    cursor.execute("INSERT INTO cart (user_id, product_id, quantity, total_amount) VALUES (?, ?, ?, ?)",
    (session['user_id'], product_id, 1, produk[2]
))
    
    connection.commit()
    connection.close()
    return redirect('/cart')

@app.route('/cart')
def carte():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cart join tb_product on cart.product_id=tb_product.id")
    cart = cursor.fetchall()
    connection.close()

    # print(cart)
    return render_template('cart.html',cart=cart,total=sum(i[4] for i in cart) )

@app.route('/delcart/<int:cart_id>')
def delcart(cart_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM cart WHERE cart_id=?", (cart_id,))
    connection.commit()
    connection.close()
    # print(cart)
    return redirect('/cart' )
    
@app.route('/updatecart/<int:cart_id>/<int:product_id>', methods=['POST'])
def updatecart(cart_id,product_id):
    connection = connect_db()
    cursor = connection.cursor()
    queryProduct =cursor.execute("SELECT * FROM tb_product WHERE id=?", (product_id,))
    produk = queryProduct.fetchone()
    cursor.execute("UPDATE cart SET quantity=?,total_amount=? WHERE cart_id=? ",
                   (request.form['quantity'],produk[2]*int(request.form['quantity']), cart_id))
    connection.commit()
    connection.close()
    # print(produk[2]*int(request.form['quantity']))
    return redirect('/cart')

@app.route('/checkout')
def check():
    connection = connect_db()
    cursor = connection.cursor()
    
    queryProduct =cursor.execute("SELECT * FROM cart WHERE user_id=?", (session['user_id'],))
    produk = queryProduct.fetchall()
    print(produk)
    for i in produk:
        cursor.execute("INSERT INTO orders (customer_id, product_id,order_date, quantity, total_amount) VALUES (?, ?, ?, ?,?)", (session['user_id'], i[2],datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i[3], i[4]))
        
    
    cursor.execute("DELETE FROM cart WHERE user_id=?", (session['user_id'],))
    connection.commit()
    connection.close()
    return redirect('/guest')

@app.route('/logadmin')
def logadmin():
    return render_template('login_admin.html')
   


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form :

#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         role_id = 2

#         connection = connect_db()
#         cursor = connection.cursor()
#         cursor.execute('SELECT * FROM users WHERE username=?', (username,))
#         existing_user = cursor.fetchone()
#         if existing_user:
#             flash('Username already exists. Please choose a different one.', 'error')
#         else:
#             cursor.execute('INSERT INTO users (username, email, password, role_id) VALUES (?, ?, ?, ?)', (username, email, password, role_id))
#             connection.commit()
#             flash('Account created successfully! Please login.', 'success')
#             connection.close()
#             return render_template('login_admin.html')

#     return render_template('register.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:

#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         role_id = 2  # Menggunakan role_id yang sesuai

#         # Pemeriksaan email dan username
#         if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address!'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers!'
#         else:
#             connection = connect_db()

#             cursor = connection.cursor()

#             # Cek apakah role dengan role_id yang diinginkan sudah ada
#             cursor.execute('SELECT * FROM roles WHERE role_id = ?', (role_id,))
#             existing_role = cursor.fetchone()
#             if existing_role =:

#             # Setelah memastikan role_id tersedia, masukkan data ke tabel users
#         cursor.execute("INSERT INTO users (username, email, password, role_id) VALUES (?, ?, ?, ?)", (username, email, password, role_id))
#         connection.commit()
#         msg = 'You have successfully registered!'
#         connection.close()

#     elif request.method == 'POST':
#         msg = 'Please fill out the form!'

#     return render_template('register.html', msg=msg)
# @app.route('/signin', methods=['GET', 'POST'])
# def user_signin():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         connection = sqlite3.connect('produk.db')
#         cursor = connection.cursor()

#         cursor.execute('SELECT * FROM users WHERE email=?', (email,))
#         user = cursor.fetchone()

#         if user and sha256_crypt.verify(password, user[2]):
#             session['user'] = email
#             flash('Login successful!', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid username or password. Please try again.', 'error')

#         connection.close()

#     return render_template('signin.html')



if __name__ == '__main__':
    app.run(debug=True)