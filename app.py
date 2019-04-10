import json
import os
import hashlib
import admin_api
import helpers
from flask import Flask, jsonify, render_template, request, session, flash, redirect
import vendor_api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']
    category = request.form['category']
    session['username'] = username
    pass_hash = hashlib.md5(password.encode())
    session['password'] = pass_hash.hexdigest()
    session['category'] = category

    status, message = helpers.check_password(username, password, category)

    if status:
        session['logged_in'] = True
    else:
        flash(message)

    return index()


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session['logged_in'] = False
    return redirect('/')


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('landing.html')
    else:
        category = session['category']
        user_id = session['username']
        if category == 'admin':
            return redirect('/api/v1/warehouse/products/{}'.format(user_id))
        elif category == 'vendor':
            return redirect('/api/v1/vendor/home/{}'.format(user_id))
        else:
            return 'Server Error.'


@app.route('/api/v1/warehouse/products/<admin_id>', methods=['GET'])
def admin_home(admin_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_admin_home_info(admin_id)
        page_info = json.dumps(page_info)
        page_info = json.loads(page_info)
        return render_template('admin_home.html',
                               products=json.dumps(page_info['products']),
                               ordered=page_info['ordered_products'],
                               admin_name=page_info['admin_name'],
                               id=admin_id,
                               t_budget=page_info['total_budget'],
                               r_budget=page_info['remaining_budget'])
    except Exception as e:
        return str(e)


@app.route('/api/v1/order/products', methods=['GET'])
def order_home():
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_order_home_info()
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/admin/info/<admin_id>', methods=['GET'])
def admin_info(admin_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_admin_info(admin_id)
        return render_template('admin_info.html', id=admin_id, info=page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/order/history/<admin_id>', methods=['GET'])
def order_history(admin_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_order_history(admin_id)
        history = []
        for info in page_info:
            data = {}
            for k, v in info.items():
                if k in ['invoice_id', 'total_cost', 'payment_status']:
                    data[k] = v
                if k in ['date_placed']:
                    data[k] = v.strftime("%m/%d/%Y  %H:%M:%S")
            history.append(data)
        return render_template('history.html', id=admin_id, info=history)
    except Exception as e:
        return str(e)


@app.route('/api/v1/invoice/info/<admin_id>/<invoice_id>', methods=['GET'])
def invoice_info(admin_id, invoice_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_invoice_info(admin_id, invoice_id)
        return render_template('invoice.html', id=admin_id, invoice_id=invoice_id, info=page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/product/info/<product_id>', methods=['GET'])
def product_info(product_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_product_info(product_id)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/place/order/<admin_id>', methods=['GET', 'POST'])
def place_order(admin_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        if request.method == 'GET':
            page_info = admin_api.fetch_admin_budget_info(admin_id)
            return render_template('order.html', id=admin_id, t_budget=page_info['total_budget'],
                                   r_budget=page_info['remaining_budget'], admin_name=page_info['admin_name'])

        elif request.method == 'POST':
            vendor_info = request.form['vendor'].split('|')
            product_id = vendor_info[3]
            vendor_product_id = vendor_info[4]
            vendor_id = vendor_info[5]
            quantity = int(request.form['quantity'])
            total_amount = float(request.form['total'])
            invoice_id = admin_api.generate_order(admin_id, product_id, vendor_product_id,
                                                  vendor_id, quantity, total_amount)
            page_info = admin_api.fetch_invoice_info(admin_id, invoice_id)
            return render_template('invoice.html', id=admin_id, invoice_id=invoice_id, info=page_info)

    except Exception as e:
        return str(e)


@app.route('/api/v1/brand/info/<category>', methods=['GET'])
def brand_info(category):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_brand_info(category)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/product_drop_down/info/<category>/<brand>', methods=['GET'])
def product_drop_down_info(category, brand):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_product_drop_down_info(category, brand)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/vendor_drop_down/info/<category>/<brand>/<product_name>', methods=['GET'])
def vendor_drop_down_info(category, brand, product_name):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_vendor_drop_down_info(category, brand, product_name)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/category_drop_down/info', methods=['GET'])
def category_drop_down_info():
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        page_info = admin_api.fetch_category_drop_down_info()
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/admin/add/product/<admin_id>', methods=['GET', 'POST'])
def add_new_product(admin_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')

        if request.method == 'GET':
            return render_template('add_product.html', id=admin_id, p_id='')

        elif request.method == 'POST':
            category = None
            info = None

            if 'category_select' in request.form:
                category = request.form['category_select']
            elif 'category_text' in request.form:
                category = request.form['category_text']

            if 'info' in request.form:
                info = request.form['info']

            brand = request.form['brand']
            name = request.form['product']
            product_id = admin_api.add_new_product(category, brand, name, info)
            return render_template('add_product.html', id=admin_id, p_id=product_id)

    except Exception as e:
        return str(e)


@app.route('/api/v1/vendor/payment_info/<vendor_id>', methods=['GET'])
def vendor_payment_info(vendor_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        page_info = vendor_api.fetch_vendor_payment_info(vendor_id)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/vendor/payment/<vendor_id>', methods=['GET'])
def vendor_payment(vendor_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        page_info = vendor_api.fetch_vendor_payment_info(vendor_id)
        page_info = json.dumps(page_info)
        page_info = json.loads(page_info)
        return render_template('vendor_payment.html',
                               type=page_info['type'],
                               account_name=page_info['account_name'],
                               account_number=page_info['account_number'],
                               routing_number=page_info['routing_number'],
                               paypal_id=page_info['paypal_id'],
                               venmo_id=page_info['venmo_id'],
                               vendor_name=page_info['vendor_name'],
                               id=vendor_id)
    except Exception as e:
        return str(e)


@app.route('/api/v1/payment/info/<vendor_id>', methods=['GET'])
def payment_info(vendor_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        page_info = vendor_api.fetch_vendor_payment_info(vendor_id)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/vendor/profile/<vendor_id>', methods=['GET'])
def vendor_profile(vendor_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        page_info = vendor_api.fetch_vendor_info(vendor_id)
        page_info = json.dumps(page_info)
        page_info = json.loads(page_info)
        return render_template('vendor_profile.html',
                               vendor_id=page_info['vendor_id'],
                               vendor_name=page_info['vendor_name'],
                               mobile=page_info['mobile'],
                               email=page_info['email'],
                               address_id=page_info['address_id'],
                               street=page_info['street'],
                               city=page_info['city'],
                               state=page_info['state'],
                               zip=page_info['zip'],
                               id=vendor_id)
    except Exception as e:
        return str(e)


@app.route('/api/v1/order/vendor_history/<vendor_id>', methods=['GET'])
def vendor_order_history(vendor_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        page_info = vendor_api.fetch_vendor_order_history(vendor_id)
        history = []
        for info in page_info:
            data = {}
            for k, v in info.items():
                if k in ['invoice_id', 'total_cost', 'payment_status']:
                    data[k] = v
                if k in ['date_placed']:
                    data[k] = v.strftime("%m/%d/%Y  %H:%M:%S")
            history.append(data)
        return render_template('vendor_history.html', id=vendor_id, info=history)
    except Exception as e:
        return str(e)


@app.route('/api/v1/vendor_invoice/info/<vendor_id>/<invoice_id>', methods=['GET'])
def vendor_invoice_info(vendor_id, invoice_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        page_info = vendor_api.fetch_vendor_invoice_info(vendor_id, invoice_id)
        return render_template('vendor_invoice.html', id=vendor_id, invoice_id=invoice_id, info=page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/add_products/<vendor_id>', methods=['GET', 'POST'])
def add_order(vendor_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        if request.method == 'GET':
            return render_template('vendor_order.html', id=vendor_id)
        elif request.method == 'POST':
            product_info = request.form['product'].split('|')
            category_info = request.form['category'].split('|')
            brand_info = request.form['brand'].split('|')
            name = product_info[0]
            category = category_info[0]
            brand = brand_info[0]
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])
            product_id = vendor_api.get_product_id(name, category, brand)
            result = vendor_api.generate_vendor_order(product_id, vendor_id,
                                                  quantity, price)
            return render_template('vendor_order.html', id=vendor_id)
    except Exception as e:
        return str(e)


@app.route('/api/v1/vendor/home/<vendor_id>', methods=['GET', 'POST'])
def vendor_home(vendor_id):
    try:
        if not session.get('logged_in'):
            return render_template('landing.html')
        if request.method == 'POST':
            product_info = request.form['product_id']
            product_id = int(product_info)

            button = request.form['submit']
            if button == "update":
                quantity_info = request.form['quantity']
                quantity = int(quantity_info)
                result = vendor_api.edit_product(vendor_id, product_id, quantity)

            else:
                result = vendor_api.delete_product(vendor_id, product_id)

            url = "/api/v1/vendor/home/" + str(vendor_id)
            return redirect(url)

        page_info = vendor_api.fetch_vendor_home_info(vendor_id)
        page_info = json.dumps(page_info)
        page_info = json.loads(page_info)
        return render_template('vendor_home.html',
                               products=json.dumps(page_info['products']),
                               vendor_name=page_info['vendor_name'],
                               id=vendor_id)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
