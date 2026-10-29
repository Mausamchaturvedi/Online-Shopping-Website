from io import BytesIO
from flask import send_file, abort
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)


from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    jsonify,
    url_for
)
from flask_bcrypt import Bcrypt
import pymysql
import os
import razorpay
from decimal import Decimal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "shopeasy123")

bcrypt = Bcrypt(app)

# Razorpay configuration
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = None

if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(
        auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
    )

# MySQL Connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="shopeasy"
)

print("APP TYPE:", type(app))
print("APP FILE:", getattr(app, "__file__", "No file attribute"))

# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template('index.html')


# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(
    password
).decode('utf-8')

        cursor = connection.cursor()

        sql = """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (name, email, hashed_password))
        connection.commit()

        return "Registration Successful"

    return render_template('register.html')


# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(
            user[3],
            password
        ):

            session['user_id'] = user[0]

            return redirect('/products')

        else:

            return "Invalid Email Or Password"

    return render_template('login.html')

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


# ---------------- PRODUCTS ----------------

# ---------------- PRODUCTS PAGE ----------------


@app.route('/products')
def products():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    cursor = connection.cursor()

    query = """
        SELECT *
        FROM products
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND name LIKE %s"
        params.append(f"%{search}%")

    if category:
        query += " AND category_id = %s"
        params.append(category)

    query += " ORDER BY id ASC"

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.execute("SELECT * FROM categories ORDER BY id ASC")
    categories = cursor.fetchall()

    cursor.close()

    return render_template(
        'products.html',
        products=data,
        categories=categories
    )



# ---------------- PRODUCT DETAILS PAGE ----------------

@app.route('/product/<int:id>')
def product_details(id):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM products
        WHERE id=%s
        """,
        (id,)
    )

    product = cursor.fetchone()

    return render_template(
        'product_details.html',
        product=product
    )

# ---------------- ADD TO CART ----------------

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO cart
        (user_id, product_id, quantity)
        VALUES (%s, %s, %s)
        """,
        (user_id, product_id, 1)
    )

    connection.commit()

    return redirect('/cart')


# ---------------- CART ----------------

# @app.route('/cart')
# def cart():

#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']

#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         SELECT
#         products.name,
#         products.price

#         FROM cart

#         JOIN products
#         ON cart.product_id = products.id

#         WHERE cart.user_id=%s
#         """,
#         (user_id,)
#     )

#     cart_items = cursor.fetchall()

#     return render_template(
#         'cart.html',
#         cart_items=cart_items
#     )


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT
            c.product_id,
            c.quantity,
            p.name,
            p.price,
            p.image,
            p.stock
        FROM cart c
        JOIN products p ON p.id = c.product_id
        WHERE c.user_id = %s
        ORDER BY c.id DESC
    """, (session['user_id'],))

    cart_items = cursor.fetchall()
    cursor.close()

    total = sum(
        float(item['price']) * int(item['quantity'] or 1)
        for item in cart_items
    )

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=total
    )


@app.route('/cart/update', methods=['POST'])
def update_cart():
    if 'user_id' not in session:
        return redirect('/login')

    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)

    if not product_id or not quantity or quantity < 1:
        return redirect('/cart')

    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.stock
        FROM cart c
        JOIN products p ON p.id = c.product_id
        WHERE c.user_id = %s AND c.product_id = %s
    """, (session['user_id'], product_id))

    result = cursor.fetchone()

    if result and result[0] is not None and quantity <= result[0]:
        cursor.execute("""
            UPDATE cart
            SET quantity = %s
            WHERE user_id = %s AND product_id = %s
        """, (quantity, session['user_id'], product_id))
        connection.commit()

    cursor.close()
    return redirect('/cart')


@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect('/login')

    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM cart
        WHERE user_id = %s AND product_id = %s
    """, (session['user_id'], product_id))

    connection.commit()
    cursor.close()

    return redirect('/cart')



# @app.route('/orders')
# def orders():

#     if 'user_id' not in session:
#         return redirect('/login')

#     user_id = session['user_id']

#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         SELECT * FROM orders
#         WHERE user_id=%s
#         ORDER BY id DESC
#         """,
#         (user_id,)
#     )

#     orders = cursor.fetchall()

#     return render_template(
#         'orders.html',
#         orders=orders
#     )

# @app.route('/orders')
# def orders():
#     if 'user_id' not in session:
#         return redirect('/login')

#     cursor = connection.cursor()
#     cursor.execute("""
#         SELECT id, total_amount, order_date
#         FROM orders
#         WHERE user_id = %s
#         ORDER BY order_date DESC
#     """, (session['user_id'],))

#     orders = cursor.fetchall()
#     cursor.close()

#     return render_template('orders.html', orders=orders)


@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect('/login')

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, total_amount, order_date, status,
               payment_method, payment_status
        FROM orders
        WHERE user_id = %s
        ORDER BY order_date DESC
    """, (session['user_id'],))

    orders = cursor.fetchall()
    cursor.close()

    return render_template('orders.html', orders=orders)


@app.route('/admin', methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM admin
            WHERE username=%s
            AND password=%s
            """,
            (username,password)
        )

        admin = cursor.fetchone()

        if admin:

            session['admin_id'] = admin[0]

            return redirect('/admin_dashboard')

        return "Invalid Admin Credentials"

    return render_template(
        'admin_login.html'
    )

@app.route('/admin/dashboard')
def admin_dashboard():

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cursor = connection.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Total Products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    # Total Orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    # Total Revenue
    cursor.execute(
        """
        SELECT IFNULL(SUM(total_amount),0)
        FROM orders
        """
    )
    total_revenue = cursor.fetchone()[0]

    # Today's Revenue
    cursor.execute(
        """
        SELECT IFNULL(SUM(total_amount),0)
        FROM orders
        WHERE DATE(order_date)=CURDATE()
        """
    )
    today_revenue = cursor.fetchone()[0]

    # This Month Revenue
    cursor.execute(
        """
        SELECT IFNULL(SUM(total_amount),0)
        FROM orders
        WHERE MONTH(order_date)=MONTH(CURDATE())
        AND YEAR(order_date)=YEAR(CURDATE())
        """
    )
    month_revenue = cursor.fetchone()[0]

    # Recent Orders
    cursor.execute(
        """
        SELECT
        orders.id,
        users.name,
        orders.total_amount,
        orders.status

        FROM orders

        JOIN users
        ON orders.user_id = users.id

        ORDER BY orders.id DESC
        LIMIT 5
        """
    )
    recent_orders = cursor.fetchall()

    # Low Stock Products
    cursor.execute(
        """
        SELECT
        id,
        name,
        stock

        FROM products

        WHERE stock <= 5

        ORDER BY stock ASC
        """
    )
    low_stock_products = cursor.fetchall()

    # Top Selling Product
    cursor.execute(
        """
        SELECT
        products.name,
        SUM(order_items.quantity) AS total_sold

        FROM order_items

        JOIN products
        ON order_items.product_id = products.id

        GROUP BY products.id

        ORDER BY total_sold DESC

        LIMIT 1
        """
    )
    top_product = cursor.fetchone()

    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        today_revenue=today_revenue,
        month_revenue=month_revenue,
        recent_orders=recent_orders,
        low_stock_products=low_stock_products,
        top_product=top_product
    )


@app.route('/logout_admin')
def logout_admin():

    session.pop(
        'admin_id',
        None
    )

    return redirect('/admin')

@app.route('/admin_products')
def admin_products():

    if 'admin_id' not in session:
        return redirect('/admin')

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    return render_template(
        'admin_products.html',
        products=products
    )

@app.route('/add_product',
methods=['GET','POST'])
def add_product():

    if 'admin_id' not in session:
        return redirect('/admin')

    if request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.form['image']
        stock = request.form['stock']

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (name,description,price,image,stock)

            VALUES(%s,%s,%s,%s,%s)
            """,
            (
             name,
             description,
             price,
             image,
             stock
            )
        )

        connection.commit()

        return redirect(
            '/admin_products'
        )

    return render_template(
        'add_product.html'
    )

@app.route('/delete_product/<int:id>')
def delete_product(id):

    if 'admin_id' not in session:
        return redirect('/admin')

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE id=%s
        """,
        (id,)
    )

    connection.commit()

    return redirect(
        '/admin_products'
    )

@app.route('/edit_product/<int:id>',
methods=['GET','POST'])
def edit_product(id):

    if 'admin_id' not in session:
        return redirect('/admin')

    cursor = connection.cursor()

    if request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.form['image']
        stock = request.form['stock']

        cursor.execute(
            """
            UPDATE products

            SET
            name=%s,
            description=%s,
            price=%s,
            image=%s,
            stock=%s

            WHERE id=%s
            """,
            (
                name,
                description,
                price,
                image,
                stock,
                id
            )
        )

        connection.commit()

        return redirect(
            '/admin_products'
        )

    cursor.execute(
        """
        SELECT * FROM products
        WHERE id=%s
        """,
        (id,)
    )

    product = cursor.fetchone()

    return render_template(
        'edit_product.html',
        product=product
    )

@app.route('/admin_users')
def admin_users():

    if 'admin_id' not in session:
        return redirect('/admin')

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users"
    )

    users = cursor.fetchall()

    return render_template(
        'admin_users.html',
        users=users
    )

@app.route('/admin_stats')
def admin_stats():

    if 'admin_id' not in session:
        return redirect('/admin')

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )
    users = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )
    products = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )
    orders = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT IFNULL(
        SUM(total_amount),0)
        FROM orders
        """
    )
    revenue = cursor.fetchone()[0]

    return f'''
    Total Users: {users}<br>
    Total Products: {products}<br>
    Total Orders: {orders}<br>
    Revenue: ₹{revenue}
    '''


# ---------------- CHECKOUT ----------------



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    cursor = connection.cursor()

    cursor.execute("""
        SELECT products.id, products.name,
               products.price, products.stock
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (user_id,))

    items = cursor.fetchall()

    if not items:
        return "Your cart is empty."

    total = sum(Decimal(str(item[2])) for item in items)

    if request.method == 'POST':
        payment_method = request.form.get('payment_method')

        if payment_method == 'COD':
            try:
                connection.begin()

                # Recheck stock and decrement safely.
                for item in items:
                    cursor.execute("""
                        UPDATE products
                        SET stock = stock - 1
                        WHERE id = %s AND stock > 0
                    """, (item[0],))

                    if cursor.rowcount != 1:
                        raise ValueError(
                            f"Product {item[1]} is out of stock."
                        )

                cursor.execute("""
                    INSERT INTO orders
                    (user_id, total_amount, status,
                     payment_method, payment_status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    user_id, total, 'Pending', 'COD', 'Pending'
                ))

                order_id = cursor.lastrowid

                for item in items:
                    cursor.execute("""
                        INSERT INTO order_items
                        (order_id, product_id, quantity, price)
                        VALUES (%s, %s, %s, %s)
                    """, (order_id, item[0], 1, item[2]))

                cursor.execute(
                    "DELETE FROM cart WHERE user_id = %s",
                    (user_id,)
                )

                connection.commit()
                return redirect(url_for('checkout_success',
                                         order_id=order_id))

            except Exception as e:
                connection.rollback()
                if isinstance(e, ValueError):
                    return str(e), 400
                app.logger.exception("COD checkout failed")
                return "Could not place your order. Please try again.", 500

        if payment_method == 'ONLINE':
            return redirect(url_for('checkout'))

        return "Invalid payment method.", 400

    return render_template(
        'checkout.html',
        total=total,
        razorpay_key_id=RAZORPAY_KEY_ID
    )


@app.route('/payment/create', methods=['POST'])
def create_payment():
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in first.'}), 401

    user_id = session['user_id']
    cursor = connection.cursor()

    cursor.execute("""
        SELECT products.id, products.name,
               products.price, products.stock
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """, (user_id,))

    items = cursor.fetchall()

    if not items:
        return jsonify({'error': 'Your cart is empty.'}), 400

    total = sum(Decimal(str(item[2])) for item in items)

    for item in items:
        if item[3] is None or item[3] <= 0:
            return jsonify({
                'error': f'{item[1]} is out of stock.'
            }), 400

    # Razorpay accepts the amount in paise, not rupees.
    amount_paise = int(total * 100)

    try:
        rp_order = razorpay_client.order.create(data={
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f'shopeasy_{user_id}_{os.urandom(4).hex()}'
        })

        connection.begin()

        cursor.execute("""
            INSERT INTO orders
            (user_id, total_amount, status, payment_method,
             payment_status, razorpay_order_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id, total, 'Pending', 'Razorpay',
            'Pending', rp_order['id']
        ))

        local_order_id = cursor.lastrowid

        for item in items:
            cursor.execute("""
                INSERT INTO order_items
                (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (local_order_id, item[0], 1, item[2]))

        connection.commit()

        return jsonify({
            'key_id': RAZORPAY_KEY_ID,
            'amount': amount_paise,
            'currency': 'INR',
            'razorpay_order_id': rp_order['id'],
            'local_order_id': local_order_id,
            'name': 'ShopEasy',
            'description': f'Order #{local_order_id}'
        })

    except Exception:
        connection.rollback()
        app.logger.exception("Payment order creation failed")
        return jsonify({
            'error': 'Unable to start payment. Please try again.'
        }), 500


@app.route('/payment/verify', methods=['POST'])
def verify_payment():
    if 'user_id' not in session:
        return jsonify({'error': 'Please log in again.'}), 401

    data = request.get_json(silent=True) or {}

    payment_id = data.get('razorpay_payment_id')
    rp_order_id = data.get('razorpay_order_id')
    signature = data.get('razorpay_signature')
    local_order_id = data.get('local_order_id')

    if not all([payment_id, rp_order_id, signature, local_order_id]):
        return jsonify({'error': 'Missing payment details.'}), 400

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, total_amount, status, payment_status
        FROM orders
        WHERE id = %s AND user_id = %s
          AND razorpay_order_id = %s
    """, (local_order_id, session['user_id'], rp_order_id))

    order = cursor.fetchone()

    if not order:
        return jsonify({'error': 'Order not found.'}), 404

    if order[3] == 'Paid':
        return jsonify({
            'success': True,
            'message': 'Payment was already verified.',
            'redirect_url': url_for(
                'checkout_success', order_id=order[0]
            )
        })

    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': rp_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        # Also confirm the payment is captured, not merely authorized.
        payment = razorpay_client.payment.fetch(payment_id)

        if payment.get('order_id') != rp_order_id:
            return jsonify({'error': 'Payment order mismatch.'}), 400

        if payment.get('status') != 'captured':
            return jsonify({
                'error': 'Payment is not captured yet. Please retry later.'
            }), 400

        if int(payment.get('amount', -1)) != int(
            Decimal(str(order[1])) * 100
        ):
            return jsonify({'error': 'Payment amount mismatch.'}), 400

        connection.begin()

        cursor.execute("""
            SELECT product_id, quantity
            FROM order_items
            WHERE order_id = %s
        """, (local_order_id,))

        order_items = cursor.fetchall()

        for product_id, quantity in order_items:
            cursor.execute("""
                UPDATE products
                SET stock = stock - %s
                WHERE id = %s AND stock >= %s
            """, (quantity, product_id, quantity))

            if cursor.rowcount != 1:
                raise ValueError(
                    "Stock changed during payment. Contact support "
                    "for assistance with your captured payment."
                )

        cursor.execute("""
            UPDATE orders
            SET status = 'Confirmed',
                payment_status = 'Paid',
                razorpay_payment_id = %s
            WHERE id = %s AND user_id = %s
              AND payment_status = 'Pending'
        """, (payment_id, local_order_id, session['user_id']))

        if cursor.rowcount != 1:
            raise ValueError("Order has already been processed.")

        cursor.execute("""
            DELETE FROM cart WHERE user_id = %s
        """, (session['user_id'],))

        connection.commit()

        return jsonify({
            'success': True,
            'message': 'Payment verified successfully.',
            'redirect_url': url_for(
                'checkout_success', order_id=local_order_id
            )
        })

    except ValueError as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 409

    except Exception:
        connection.rollback()
        app.logger.exception("Payment verification failed")
        return jsonify({
            'error': 'Payment verification failed. Contact support '
                     'if money was deducted.'
        }), 400


@app.route('/checkout/success/<int:order_id>')
def checkout_success(order_id):
    if 'user_id' not in session:
        return redirect('/login')

    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, total_amount, status, payment_method, payment_status
        FROM orders
        WHERE id = %s AND user_id = %s
    """, (order_id, session['user_id']))

    order = cursor.fetchone()

    if not order:
        return "Order not found.", 404

    return render_template('checkout_success.html', order=order)




@app.route('/my_orders')
def my_orders():

    if 'user_id' not in session:
        return redirect('/login')

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM orders
        WHERE user_id=%s
        """,
        (session['user_id'],)
    )

    orders = cursor.fetchall()

    return render_template(
        'orders.html',
        orders=orders
    )

@app.route('/order/<int:order_id>')
def order_details(order_id):

    if 'user_id' not in session:
        return redirect('/login')

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
        products.name,
        order_items.quantity,
        order_items.price

        FROM order_items

        JOIN products
        ON order_items.product_id = products.id

        WHERE order_items.order_id=%s
        """,
        (order_id,)
    )

    items = cursor.fetchall()

    return render_template(
        'order_details.html',
        items=items,
        order_id=order_id
    )

@app.route('/admin/orders')
def admin_orders():

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
        orders.id,
        users.name,
        users.email,
        orders.total_amount,
        orders.order_date,
        orders.status

        FROM orders

        JOIN users
        ON orders.user_id = users.id

        ORDER BY orders.id DESC
        """
    )

    orders = cursor.fetchall()

    return render_template(
        'admin_orders.html',
        orders=orders
    )

@app.route('/admin/order/<int:order_id>')
def admin_order_details(order_id):

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
        products.name,
        order_items.quantity,
        order_items.price

        FROM order_items

        JOIN products
        ON order_items.product_id = products.id

        WHERE order_items.order_id=%s
        """,
        (order_id,)
    )

    items = cursor.fetchall()

    return render_template(
        'order_details.html',
        items=items,
        order_id=order_id
    )


@app.route('/update_order_status/<int:id>/<status>')
def update_order_status(id, status):

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status=%s
        WHERE id=%s
        """,
        (status, id)
    )

    connection.commit()

    return redirect('/admin_orders')

# @app.route('/invoice/<int:order_id>')
# def invoice(order_id):

#     if 'user_id' not in session:
#         return redirect('/login')

#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         SELECT
#         products.name,
#         order_items.quantity,
#         order_items.price

#         FROM order_items

#         JOIN products
#         ON order_items.product_id = products.id

#         WHERE order_items.order_id=%s
#         """,
#         (order_id,)
#     )

#     items = cursor.fetchall()

#     cursor.execute(
#         """
#         SELECT
#         total_amount,
#         order_date

#         FROM orders

#         WHERE id=%s
#         """,
#         (order_id,)
#     )

#     order = cursor.fetchone()

#     return render_template(
#         'invoice.html',
#         items=items,
#         order=order,
#         order_id=order_id
#     )


@app.route('/invoice/<int:order_id>')
def download_invoice(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = connection.cursor()

    # Fetch only an order belonging to the logged-in user
    cursor.execute("""
        SELECT id, total_amount, order_date, status,
               payment_method, payment_status
        FROM orders
        WHERE id = %s AND user_id = %s
    """, (order_id, session['user_id']))

    order = cursor.fetchone()

    if not order:
        cursor.close()
        abort(404)

    # Fetch products included in this order
    cursor.execute("""
        SELECT p.name, oi.quantity, oi.price
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        WHERE oi.order_id = %s
    """, (order_id,))

    items = cursor.fetchall()
    cursor.close()

    # Create the PDF in memory
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(
        "<b>ShopEasy</b>", styles["Title"]
    ))
    story.append(Paragraph(
        "ORDER INVOICE / PAYMENT RECEIPT",
        styles["Heading2"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        f"<b>Invoice No:</b> SE-{order[0]}",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"<b>Order Date:</b> {order[2]}",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"<b>Order Status:</b> {order[3] or 'Pending'}",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"<b>Payment Method:</b> {order[4] or 'Not specified'}",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"<b>Payment Status:</b> {order[5] or 'Pending'}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 18))

    table_data = [
        ["Product", "Quantity", "Unit Price (INR)", "Amount (INR)"]
    ]

    for item in items:
        name, quantity, price = item
        line_total = float(quantity) * float(price)

        table_data.append([
            str(name),
            str(quantity),
            f"Rs. {float(price):,.2f}",
            f"Rs. {line_total:,.2f}"
        ])

    table_data.append([
        "", "", "TOTAL",
        f"Rs. {float(order[1]):,.2f}"
    ])

    table = Table(
        table_data,
        colWidths=[72 * mm, 22 * mm, 35 * mm, 35 * mm],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (2, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E5E7EB")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(table)
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "Thank you for shopping with ShopEasy!",
        styles["Heading3"]
    ))
    story.append(Paragraph(
        "This document was generated electronically.",
        styles["Normal"]
    ))

    doc.build(story)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"ShopEasy_Invoice_{order_id}.pdf"
    )

@app.route('/payment/create', methods=['POST'])
def payment_create():
    if 'user_id' not in session:
        return jsonify(error="Please log in again."), 401

    if razorpay_client is None:
        return jsonify(error="Razorpay keys are not configured."), 500

    cursor = connection.cursor()

    try:
        user_id = session['user_id']

        cursor.execute("""
            SELECT p.id, p.price, p.stock
            FROM cart c
            JOIN products p ON p.id = c.product_id
            WHERE c.user_id = %s
        """, (user_id,))
        items = cursor.fetchall()

        if not items:
            return jsonify(error="Your cart is empty."), 400

        total_paise = sum(round(float(item[1]) * 100) for item in items)

        if total_paise <= 0:
            return jsonify(error="Invalid order amount."), 400

        if any(item[2] is None or item[2] <= 0 for item in items):
            return jsonify(error="A product is out of stock."), 400

        # Create the Razorpay order on the server.
        rz_order = razorpay_client.order.create({
            "amount": total_paise,
            "currency": "INR",
            "receipt": "user_" + str(user_id)
        })

        cursor.execute("""
            INSERT INTO orders
            (user_id, total_amount, payment_method, payment_status,
             razorpay_order_id, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            total_paise / 100,
            'ONLINE',
            'Pending',
            rz_order['id'],
            'Pending'
        ))

        connection.commit()

        return jsonify(
            key_id=RAZORPAY_KEY_ID,
            amount=rz_order['amount'],
            currency='INR',
            name='ShopEasy',
            description='ShopEasy order payment',
            razorpay_order_id=rz_order['id'],
            local_order_id=cursor.lastrowid
        )

    except Exception:
        connection.rollback()
        app.logger.exception("Could not create payment order")
        return jsonify(error="Could not start payment. Please try again."), 500


@app.route('/payment/verify', methods=['POST'])
def payment_verify():
    if 'user_id' not in session:
        return jsonify(success=False, error="Please log in again."), 401

    if razorpay_client is None:
        return jsonify(success=False, error="Razorpay is not configured."), 500

    data = request.get_json(silent=True) or {}

    payment_id = data.get('razorpay_payment_id')
    rz_order_id = data.get('razorpay_order_id')
    signature = data.get('razorpay_signature')
    local_order_id = data.get('local_order_id')
    user_id = session['user_id']

    if not all([payment_id, rz_order_id, signature, local_order_id]):
        return jsonify(success=False, error="Missing payment details."), 400

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, total_amount, payment_status, razorpay_order_id
            FROM orders
            WHERE id = %s AND user_id = %s
        """, (local_order_id, user_id))
        order = cursor.fetchone()

        if not order or order[3] != rz_order_id:
            return jsonify(success=False, error="Order not found."), 400

        if order[2] == 'Paid':
            return jsonify(success=True, redirect_url='/orders')

        # Verify the signature using the server-side SDK.
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': rz_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        # Also confirm Razorpay reports this payment as captured.
        payment = razorpay_client.payment.fetch(payment_id)

        if payment.get('order_id') != rz_order_id:
            return jsonify(success=False, error="Payment order mismatch."), 400

        if payment.get('status') != 'captured':
            return jsonify(
                success=False,
                error="Payment is not captured yet. Please retry."
            ), 400

        if int(payment.get('amount', 0)) != round(float(order[1]) * 100):
            return jsonify(success=False, error="Payment amount mismatch."), 400

        # Lock and recheck cart stock before finalizing the order.
        cursor.execute("""
            SELECT p.id, p.price, p.stock
            FROM cart c
            JOIN products p ON p.id = c.product_id
            WHERE c.user_id = %s
            FOR UPDATE
        """, (user_id,))
        items = cursor.fetchall()

        if not items:
            connection.rollback()
            return jsonify(success=False, error="Cart is empty."), 400

        if any(item[2] is None or item[2] <= 0 for item in items):
            connection.rollback()
            return jsonify(
                success=False,
                error="A product is out of stock. Contact support."
            ), 409

        cursor.execute("""
            SELECT IFNULL(SUM(price * quantity), 0)
            FROM order_items
            WHERE order_id = %s
        """, (local_order_id,))
        existing_items_total = float(cursor.fetchone()[0])

        # Avoid duplicating order items if this callback is retried.
        if existing_items_total == 0:
            for item in items:
                cursor.execute("""
                    UPDATE products
                    SET stock = stock - 1
                    WHERE id = %s AND stock > 0
                """, (item[0],))

                if cursor.rowcount != 1:
                    raise ValueError("Product stock changed.")

                cursor.execute("""
                    INSERT INTO order_items
                    (order_id, product_id, quantity, price)
                    VALUES (%s, %s, 1, %s)
                """, (local_order_id, item[0], item[1]))

        cursor.execute("""
            UPDATE orders
            SET payment_status = 'Paid',
                status = 'Confirmed',
                razorpay_payment_id = %s
            WHERE id = %s AND user_id = %s
              AND payment_status = 'Pending'
        """, (payment_id, local_order_id, user_id))

        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        connection.commit()

        return jsonify(success=True, redirect_url='/orders')

    except razorpay.errors.SignatureVerificationError:
        connection.rollback()
        return jsonify(success=False, error="Payment signature is invalid."), 400

    except Exception:
        connection.rollback()
        app.logger.exception("Payment verification failed")
        return jsonify(
            success=False,
            error="Unable to verify payment. Please contact support if charged."
        ), 500


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)