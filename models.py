import constants

from app import db


class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.String(), primary_key=True)
    product_name = db.Column(db.String(), nullable=False)
    brand = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    product_info = db.Column(db.Text())

    def __init__(self, product_id, product_name, brand, category, info=None):
        self.product_id = product_id
        self.product_name = product_name
        self.brand = brand
        self.category = category
        self.product_info = info

    def __repr__(self):
        return '<{} {}>'.format(constants.PRODUCT_INFO, self.product_id)

    def serialize(self):
        return {
            constants.PRODUCT_ID: self.product_id,
            constants.PRODUCT_NAME: self.product_name,
            constants.BRAND: self.brand,
            constants.CATEGORY: self.category,
            constants.PRODUCT_INFO: self.product_info
        }


class Vendor(db.Model):
    __tablename__ = 'vendor'

    vendor_id = db.Column(db.String(), primary_key=True)
    vendor_name = db.Column(db.String(), nullable=False)
    mobile = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    address_id = db.Column(db.String(), db.ForeignKey('address.address_id'), nullable=False, unique=True)
    payment_id = db.Column(db.String(), db.ForeignKey('payment.payment_id'), nullable=False, unique=True)

    def __init__(self, vendor_id, vendor_name, mobile, email, address_id, payment_id):
        self.vendor_id = vendor_id
        self.vendor_name = vendor_name
        self.mobile = mobile
        self.email = email
        self.address_id = address_id
        self.payment_id = payment_id

    def __repr__(self):
        return '{} {}'.format(constants.VENDOR_ID, self.vendor_id)

    def serialize(self):
        return {
            constants.VENDOR_ID: self.vendor_id,
            constants.VENDOR_NAME: self.vendor_name,
            constants.MOBILE: self.mobile,
            constants.EMAIL: self.email,
            constants.ADDRESS_ID: self.address_id,
            constants.PAYMENT_ID: self.payment_id
        }


class VendorProduct(db.Model):
    __tablename__ = 'vendor_product'

    vendor_product_id = db.Column(db.String(), primary_key=True)
    product_id = db.Column(db.String(), db.ForeignKey('product.product_id'), nullable=False)
    vendor_id = db.Column(db.String(), db.ForeignKey('vendor.vendor_id'), nullable=False)
    quantity = db.Column(db.BIGINT(), nullable=False)
    date_added = db.Column(db.TIMESTAMP(), nullable=False)
    price = db.Column(db.NUMERIC(20), nullable=False)
    db.CheckConstraint('price > 0', name='check_price')

    def __init__(self, vp_id, p_id, v_id, qty, date, price):
        self.vendor_product_id = vp_id
        self.product_id = p_id
        self.vendor_id = v_id
        self.quantity = qty
        self.date_added = date
        self.price = price

    def __repr__(self):
        return '{} {}'.format(constants.VENDOR_PRODUCT_ID, self.vendor_product_id)

    def serialize(self):
        return {
            constants.VENDOR_PRODUCT_ID: self.vendor_product_id,
            constants.PRODUCT_ID: self.product_id,
            constants.VENDOR_ID: self.vendor_id,
            constants.QUANTITY: self.quantity,
            constants.DATE_ADDED: self.date_added,
            constants.PRICE: self.price
        }


class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.String(), primary_key=True)
    admin_name = db.Column(db.String(), nullable=False)
    mobile = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    dob = db.Column(db.DATE(), nullable=False)
    address_id = db.Column(db.String(), db.ForeignKey('address.address_id'), nullable=False, unique=True)
    warehouse_id = db.Column(db.String(), nullable=False)
    budget = db.Column(db.NUMERIC(20), nullable=False)
    db.CheckConstraint('budget > 0', name='check_budget')

    def __init__(self, admin_id, admin_name, mobile, email, dob, add_id, w_id, budget):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.mobile = mobile
        self.email = email
        self.dob = dob,
        self.address_id = add_id
        self.warehouse_id = w_id
        self.budget = budget

    def __repr__(self):
        return '{} {}'.format(constants.ADMIN_ID, self.admin_id)

    def serialize(self):
        return {
            constants.ADMIN_ID: self.admin_id,
            constants.ADMIN_NAME: self.admin_name,
            constants.MOBILE: self.mobile,
            constants.EMAIL: self.email,
            constants.DOB: self.dob,
            constants.ADDRESS_ID: self.address_id,
            constants.WAREHOUSE_ID: self.warehouse_id,
            constants.BUDGET: self.budget
        }


class PlacedOrder(db.Model):
    __tablename__ = 'placed_order'

    invoice_id = db.Column(db.String(), primary_key=True)
    admin_id = db.Column(db.String(), db.ForeignKey('admin.admin_id'), nullable=False)
    vendor_id = db.Column(db.String(), nullable=False)
    warehouse_id = db.Column(db.String(), nullable=False)
    product_id = db.Column(db.String(), nullable=False)
    payment_status = db.Column(db.String(), nullable=False)
    price = db.Column(db.NUMERIC(20), nullable=False)
    quantity = db.Column(db.BIGINT(), nullable=False)
    date_placed = db.Column(db.TIMESTAMP(), nullable=False)
    db.CheckConstraint('price > 0', name='check_order_price')

    def __init__(self, invoice_id, admin_id, v_id, w_id, p_id, status, price, qty, date):
        self.invoice_id = invoice_id
        self.admin_id = admin_id
        self.vendor_id = v_id
        self.warehouse_id = w_id
        self.product_id = p_id
        self.payment_status = status
        self.price = price
        self.quantity = qty
        self.date_placed = date

    def __repr__(self):
        return '{} {}'.format(constants.INVOICE_ID, self.invoice_id)

    def serialize(self):
        return {
            constants.INVOICE_ID: self.invoice_id,
            constants.ADMIN_ID: self.admin_id,
            constants.VENDOR_ID: self.vendor_id,
            constants.WAREHOUSE_ID: self.warehouse_id,
            constants.PRODUCT_ID: self.product_id,
            constants.PAYMENT_STATUS: self.payment_status,
            constants.PRICE: self.price,
            constants.QUANTITY: self.quantity,
            constants.DATE_PLACED: self.date_placed
        }


class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.String(), primary_key=True)
    type = db.Column(db.String(), nullable=False)
    account_name = db.Column(db.String())
    account_number = db.Column(db.String())
    routing_number = db.Column(db.String())
    paypal_id = db.Column(db.String())
    venmo_id = db.Column(db.String())

    def __init__(self, payment_id, type, acc_name=None, acc_num=None, routing_num=None, paypal_id=None, venmo_id=None):
        self.payment_id = payment_id
        self.type = type
        self.account_name = acc_name
        self.account_number = acc_num
        self.routing_number = routing_num
        self.paypal_id = paypal_id
        self.venmo_id = venmo_id

    def __repr__(self):
        return '{} {}'.format(constants.PAYMENT_ID, self.payment_id)

    def serialize(self):
        return {
            constants.PAYMENT_ID: self.payment_id,
            constants.TYPE: self.type,
            constants.ACCOUNT_NAME: self.account_name,
            constants.ACCOUNT_NUMBER: self.account_number,
            constants.ROUTING_NUMBER: self.routing_number,
            constants.PAYPAL_ID: self.paypal_id,
            constants.VENMO_ID: self.venmo_id
        }


class Address(db.Model):
    __tablename__ = 'address'

    address_id = db.Column(db.String(), primary_key=True)
    street = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    zip_code = db.Column(db.BIGINT(), nullable=False)

    def __init__(self, add_id, st, city, state, code):
        self.address_id = add_id
        self.street = st
        self.city = city
        self.state = state
        self.zip_code = code

    def __repr__(self):
        return '{} {}'.format(constants.ADDRESS_ID, self.address_id)

    def serialize(self):
        return {
            constants.ADDRESS_ID: self.address_id,
            constants.STREET: self.street,
            constants.CITY: self.city,
            constants.STATE: self.state,
            constants.ZIP_CODE: self.zip_code
        }


class Warehouse(db.Model):
    __tablename__ = 'warehouse'

    warehouse_id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    admin_id = db.Column(db.String(), db.ForeignKey('admin.admin_id'), nullable=False, unique=True)
    address_id = db.Column(db.String(), db.ForeignKey('address.address_id'), nullable=False, unique=True)

    def __init__(self, w_id, name, admin_id, add_id):
        self.warehouse_id = w_id
        self.name = name
        self.admin_id = admin_id
        self.address_id = add_id

    def __repr__(self):
        return '{} {}'.format(constants.WAREHOUSE_ID, self.warehouse_id)

    def serialize(self):
        return {
            constants.WAREHOUSE_ID: self.warehouse_id,
            constants.NAME: self.name,
            constants.ADMIN_ID: self.admin_id,
            constants.ADDRESS_ID: self.address_id
        }


class WarehouseProduct(db.Model):
    __tablename__ = 'warehouse_product'

    warehouse_product_id = db.Column(db.String(), primary_key=True)
    product_id = db.Column(db.String(), db.ForeignKey('product.product_id'), nullable=False)
    invoice_id = db.Column(db.String(), nullable=False)
    warehouse_id = db.Column(db.String(), db.ForeignKey('warehouse.warehouse_id'), nullable=False)
    status = db.Column(db.String(), nullable=False)
    date_received = db.Column(db.TIMESTAMP(), nullable=False)

    def __repr__(self):
        return '{} {}'.format(constants.WAREHOUSE_PRODUCT_ID, self.warehouse_product_id)

    def serialize(self):
        return {
            constants.WAREHOUSE_PRODUCT_ID: self.warehouse_product_id,
            constants.PRODUCT_ID: self.product_id,
            constants.INVOICE_ID: self.invoice_id,
            constants.WAREHOUSE_ID: self.warehouse_id,
            constants.STATUS: self.status,
            constants.DATE_RECEIVED: self.date_received
        }
