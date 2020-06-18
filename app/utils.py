import hashlib

import requests

TIMEOUT_TIME = 5
EUR_CURRENCY = 978
USD_CURRENCY = 840
RUB_CURRENCY = 643

SHOP_ID = 5
SHOP_SECRET_KEY = 'SecretKey01'


def create_sign(data, fields):
    if data:
        sorted_fields = sorted(fields)
        str_for_sign = ':'.join(
            str(data[key]) for key in sorted_fields
        ) + SHOP_SECRET_KEY
        return hashlib.sha256(str_for_sign.encode()).hexdigest()
    return ""


def get_data(data, fields, url):
    sign = create_sign(data, fields)
    response = requests.post(
        url, json={**data, "sign": sign},
        headers={'Content-Type': 'application/json'},
        timeout=TIMEOUT_TIME
    )
    if response.status_code != 200:
        raise Exception
    return response.json()['data']
