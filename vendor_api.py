import constants
import vendor_sql_queries as vsq
import uuid
import datetime
import helpers
from sqlalchemy import *


engine = create_engine('postgresql:///inventory_management_system')
conn = engine.connect()

def fetch_vendor_home_info(vendor_id):
    home_page_info = {}
    records = conn.execute(vsq.vendor_query_2.format(vendor_id))
    products = helpers.generate_json_results(records)
    home_page_info['products'] = products
    records = conn.execute(vsq.vendor_query_1.format(vendor_id))
    vendor_info = helpers.generate_json_results(records)[0]
    vendor_name = vendor_info[constants.VENDOR_NAME]
    home_page_info['vendor_name'] = str(vendor_name)
    return home_page_info


def fetch_vendor_info(vendor_id):
    home_page_info = {}
    records = conn.execute(vsq.vendor_query_1.format(vendor_id))
    vendor_info = helpers.generate_json_results(records)[0]
    vendor_name = vendor_info[constants.VENDOR_NAME]
    home_page_info['vendor_name'] = str(vendor_name)
    vendor_id = vendor_info[constants.VENDOR_ID]
    home_page_info['vendor_id'] = str(vendor_id)
    mobile = vendor_info[constants.MOBILE]
    home_page_info['mobile'] = str(mobile)
    email = vendor_info[constants.EMAIL]
    home_page_info['email'] = str(email)
    address_id = vendor_info[constants.ADDRESS_ID]
    home_page_info['address_id'] = str(address_id)
    street = vendor_info['vendor_street']
    home_page_info['street'] = str(street)
    city = vendor_info['vendor_city']
    home_page_info['city'] = str(city)
    state = vendor_info['vendor_state']
    home_page_info['state'] = str(state)
    zip = vendor_info['vendor_zipcode']
    home_page_info['zip'] = str(zip)
    return home_page_info

def fetch_vendor_payment_info(vendor_id):
    home_page_info = {}
    records = conn.execute(vsq.vendor_query_1.format(vendor_id))
    vendor_info = helpers.generate_json_results(records)[0]
    vendor_name = vendor_info[constants.VENDOR_NAME]
    home_page_info['vendor_name'] = str(vendor_name)
    records = conn.execute(vsq.vendor_query_3.format(vendor_id))
    payment_info = helpers.generate_json_results(records)[0]
    type = payment_info['type']
    home_page_info['type'] = str(type)
    account_name = payment_info['account_name']
    if account_name == "":
        account_name = "NA"
    home_page_info['account_name'] = str(account_name)
    account_number = payment_info['account_number']
    if account_number == "":
        account_number = "NA"
    home_page_info['account_number'] = str(account_number)
    routing_number = payment_info['routing_number']
    if routing_number == "":
        routing_number = "NA"
    home_page_info['routing_number'] = str(routing_number)
    paypal_id = payment_info['paypal_id']
    if paypal_id == "":
        paypal_id = "NA"
    home_page_info['paypal_id'] = str(paypal_id)
    venmo_id = payment_info['venmo_id']
    if venmo_id == "":
        venmo_id = "NA"
    home_page_info['venmo_id'] = str(venmo_id)
    return home_page_info

def fetch_vendor_order_history(vendor_id):
    records = conn.execute(vsq.vendor_query_6.format(vendor_id))
    order_history = helpers.generate_json_results(records)
    return order_history

def fetch_vendor_invoice_info(vendor_id, invoice_id):
    records = conn.execute(vsq.vendor_query_8.format(vendor_id, invoice_id))
    invoice = helpers.generate_json_results(records)[0]

    invoice['date_placed'] = invoice['date_placed'].strftime("%m/%d/%Y  %H:%M:%S")
    records = conn.execute(vsq.vendor_query_9.format(invoice['admin_id']))
    warehouse_info = helpers.generate_json_results(records)[0]

    records = conn.execute(vsq.vendor_query_10.format(vendor_id))
    vendor_info = helpers.generate_json_results(records)[0]
    return {'order_info': invoice, 'warehouse_info': warehouse_info, 'vendor_info': vendor_info}

def generate_vendor_order(product_id, vendor_id, quantity, price):
    vendor_product_id = uuid.uuid4().hex
    current_time = datetime.datetime.now()
    date_placed = current_time.strftime("%Y-%m-%d %H:%M:%S")
    result = conn.execute(vsq.vendor_query_5.format(vendor_product_id=vendor_product_id, product_id=product_id, vendor_id=vendor_id, quantity=quantity, date_added=date_placed,price=price))
    return result

def get_product_id(name, category, brand):
    records =conn.execute(vsq.vendor_query_11.format(category=category, product_name=name, brand=brand))
    product_info = helpers.generate_json_results(records)[0]
    product_id = product_info['product_id']
    return product_id

def edit_product(vendor_id, product_id, quantity):
    records = conn.execute(vsq.vendor_query_12.format(vendor_id=vendor_id, product_id=product_id, quantity=quantity ))
    return records


def delete_product(vendor_id, product_id):
    records = conn.execute(vsq.vendor_query_13.format(vendor_id=vendor_id, product_id=product_id ))
    return records

