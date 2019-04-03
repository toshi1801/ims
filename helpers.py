import constants


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
