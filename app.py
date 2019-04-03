import os
import admin_api
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
        return jsonify(page_info)
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
        return jsonify(page_info)
    except Exception as e:
        return str(e)


@app.route('/api/v1/order/history/<admin_id>', methods=['GET'])
def order_history(admin_id):
    try:
        page_info = admin_api.fetch_order_history(admin_id)
        return jsonify(page_info)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
