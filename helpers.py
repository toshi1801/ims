import constants
import json
import hashlib


def generate_json_results(results):

    records = []

    for result in results:
        record = {}
        for k, v in result.items():
            if k in [constants.PRICE, constants.BUDGET, constants.TOTAL_COST]:
                record[k] = float(v)
            else:
                record[k] = v
        records.append(record)

    return records


def load_user_credentials():

    with open('user_info.txt', 'r') as file:
        data = json.load(file)

    return data


def check_password(username, password, category):

    info = load_user_credentials()

    if category in info:
        if username in info[category]:
            pass_hash = hashlib.md5(password.encode())
            if pass_hash.hexdigest() == info[category][username]:
                return True, 'Success'
            else:
                return False, 'Invalid username or password.'
        else:
            return False, "User doesn't exist."
    else:
        return False, "Server Error."
