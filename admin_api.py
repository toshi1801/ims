import constants
import datetime
import uuid
import sql_queries as sq
import helpers
from sqlalchemy import *


engine = create_engine('postgresql:///inventory_management_system')
conn = engine.connect()


def fetch_admin_home_info(admin_id):
    records = conn.execute(sq.admin_query_1.format(admin_id))
    home_page_info = {}
    products = helpers.generate_json_results(records)
    home_page_info['products'] = products

    records = conn.execute(sq.admin_query_2.format(admin_id))
    admin_info = helpers.generate_json_results(records)[0]
    admin_name = admin_info[constants.ADMIN_NAME]

    records = conn.execute(sq.admin_query_3.format(id=admin_id))
    budget_info = helpers.generate_json_results(records)[0]

    home_page_info['total_budget'] = float(budget_info[constants.BUDGET])
    if budget_info['remaining_balance']:
        home_page_info['remaining_budget'] = float(budget_info['remaining_balance'])
    else:
        home_page_info['remaining_budget'] = float(budget_info[constants.BUDGET])
    home_page_info['admin_name'] = str(admin_name)

    return home_page_info


def fetch_order_home_info():
    records = conn.execute(sq.admin_query_4)
    products = {'products': helpers.generate_json_results(records)}
    return products


def fetch_admin_budget_info(admin_id):
    info = {}
    records = conn.execute(sq.admin_query_2.format(admin_id))
    admin_info = helpers.generate_json_results(records)[0]
    admin_name = admin_info[constants.ADMIN_NAME]

    records = conn.execute(sq.admin_query_3.format(id=admin_id))
    budget_info = helpers.generate_json_results(records)[0]

    info['total_budget'] = float(budget_info[constants.BUDGET])
    if budget_info['remaining_balance']:
        info['remaining_budget'] = float(budget_info['remaining_balance'])
        info['admin_name'] = str(admin_name)
    else:
        info['remaining_budget'] = float(budget_info[constants.BUDGET])
        info['admin_name'] = str(admin_name)
    return info


def generate_order(admin_id, product_id, vendor_product_id, vendor_id, quantity, total_amount):
    """ Update vendor product info(quantity) after order is placed.

    :return:
    """
    invoice_id = uuid.uuid4().hex
    records = conn.execute(sq.admin_query_14.format(admin_id))
    warehouse_id = helpers.generate_json_results(records)[0]['warehouse_id']
    payment_status = "in progress"
    current_time = datetime.datetime.now()
    date_placed = current_time.strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(sq.admin_query_15.format(invoice_id=invoice_id, admin_id=admin_id, vendor_id=vendor_id,
                                          warehouse_id=warehouse_id, product_id=product_id,
                                          payment_status=payment_status, price=total_amount, quantity=quantity,
                                          date_placed=date_placed))
    conn.execute(sq.admin_query_16.format(quantity, vendor_product_id))
    return invoice_id


def fetch_admin_info(admin_id):
    records = conn.execute(sq.admin_query_5.format(admin_id))
    admin_info = helpers.generate_json_results(records)[0]
    admin_info['dob'] = admin_info['dob'].strftime("%m/%d/%Y")
    return admin_info


def fetch_order_history(admin_id):
    records = conn.execute(sq.admin_query_6.format(admin_id))
    order_history = helpers.generate_json_results(records)
    return order_history


def fetch_invoice_info(admin_id, invoice_id):
    records = conn.execute(sq.admin_query_8.format(admin_id, invoice_id))
    invoice = helpers.generate_json_results(records)[0]

    invoice['date_placed'] = invoice['date_placed'].strftime("%m/%d/%Y  %H:%M:%S")

    records = conn.execute(sq.admin_query_9.format(admin_id))
    warehouse_info = helpers.generate_json_results(records)[0]

    records = conn.execute(sq.admin_query_10.format(invoice['vendor_id']))
    vendor_info = helpers.generate_json_results(records)[0]
    return {'order_info': invoice, 'warehouse_info': warehouse_info, 'vendor_info': vendor_info}


def fetch_product_info(product_id):
    records = conn.execute(sq.admin_query_7.format(product_id))
    product_info = helpers.generate_json_results(records)
    return product_info[0]


def fetch_brand_info(category):
    records = conn.execute(sq.admin_query_11.format(category))
    brands = helpers.generate_json_results(records)
    brand_info = []
    for brand in brands:
        info = {"id": brand['brand'], "name": brand['brand']}
        brand_info.append(info)
    return brand_info


def fetch_product_drop_down_info(category, brand):
    records = conn.execute(sq.admin_query_12.format(category, brand))
    products = helpers.generate_json_results(records)
    product_list = []
    for product in products:
        info = {"id": product['product_name'], "name": product['product_name']}
        product_list.append(info)
    return product_list


def fetch_vendor_drop_down_info(category, brand, product_name):
    records = conn.execute(sq.admin_query_13.format(category, brand, product_name))
    vendors = helpers.generate_json_results(records)
    vendor_list = []
    print(vendors)
    for vendor in vendors:
        val = vendor['vendor_name'] + " | Qt:" + str(vendor['quantity']) + " | Price:" + str(vendor['price'])
        info = {"id": val + "|" + vendor['product_id'] + "|" + vendor['vendor_product_id'] + "|" + vendor['vendor_id'],
                "name": val}
        vendor_list.append(info)
    return vendor_list
