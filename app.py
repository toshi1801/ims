import json
import os
import admin_api
from flask_login import LoginManager
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
login = LoginManager(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/api/v1/warehouse/products/<admin_id>', methods=['GET'])
def admin_home(admin_id):
    try:
        page_info = admin_api.fetch_admin_home_info(admin_id)
        page_info = json.dumps(page_info)
        page_info = json.loads(page_info)
        return render_template('admin_home.html',
                               products=json.dumps(page_info['products']),
                               admin_name=page_info['admin_name'],
                               id=admin_id,
                               t_budget=page_info['total_budget'],
                               r_budget=page_info['remaining_budget'])
    except Exception as e:
        return str(e)


@app.route('/api/v1/order/products', methods=['GET'])
def order_home():
    try:
        page_info = admin_api.fetch_order_home_info()
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/admin/info/<admin_id>', methods=['GET'])
def admin_info(admin_id):
    try:
        page_info = admin_api.fetch_admin_info(admin_id)
        return render_template('admin_info.html', id=admin_id, info=page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/order/history/<admin_id>', methods=['GET'])
def order_history(admin_id):
    try:
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
        page_info = admin_api.fetch_invoice_info(admin_id, invoice_id)
        return render_template('invoice.html', id=admin_id, invoice_id=invoice_id, info=page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/product/info/<product_id>', methods=['GET'])
def product_info(product_id):
    try:
        page_info = admin_api.fetch_product_info(product_id)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/place/order/<admin_id>', methods=['GET', 'POST'])
def place_order(admin_id):
    try:
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
        page_info = admin_api.fetch_brand_info(category)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/product_drop_down/info/<category>/<brand>', methods=['GET'])
def product_drop_down_info(category, brand):
    try:
        page_info = admin_api.fetch_product_drop_down_info(category, brand)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/vendor_drop_down/info/<category>/<brand>/<product_name>', methods=['GET'])
def vendor_drop_down_info(category, brand, product_name):
    try:
        page_info = admin_api.fetch_vendor_drop_down_info(category, brand, product_name)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
