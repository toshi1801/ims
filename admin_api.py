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
    order_history = {'order_history': helpers.generate_json_results(records)}
    return order_history
