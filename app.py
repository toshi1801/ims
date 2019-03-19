import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Payment, Product, VendorProduct, Vendor, Warehouse, WarehouseProduct, Address, Admin, PlacedOrder


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/getall")
def get_all():
    try:
        books = Product.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
