import constants
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


def update_product_info():
    """ Update vendor product info(quantity) after order is placed.

    :return:
    """
    pass


def fetch_admin_info(admin_id):
    records = conn.execute(sq.admin_query_5.format(admin_id))
    admin_info = {'admin_info': helpers.generate_json_results(records)[0]}
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
    for vendor in vendors:
        info = {"id": {"vendor_name": vendor['vendor_name'], "quantity": vendor['quantity'], "price": vendor['price']},
                "name": vendor['vendor_name'] + " | Qt:" + str(vendor['quantity']) + " | Price:" + str(vendor['price'])}
        vendor_list.append(info)
    return vendor_list
