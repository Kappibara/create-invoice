import requests
from flask import redirect

from app.utils import TIMEOUT_TIME, USD_CURRENCY, SHOP_ID, create_sign

PIASTIX_BILL_URL = 'https://core.piastrix.com/bill/create'

REQUIRED_FIELDS_BILL = [
    'payer_currency', 'shop_amount',
    'shop_currency', 'shop_id', 'shop_order_id'
]


def get_bill_protocol(form, payment):
    data = {
        "payer_currency": USD_CURRENCY,
        "shop_amount": float(form.amount.data),
        "shop_currency": USD_CURRENCY,
        "shop_id": SHOP_ID,
        "shop_order_id": payment.shop_order_id,
    }
    sign = create_sign(data, REQUIRED_FIELDS_BILL)

    answer = requests.post(
        PIASTIX_BILL_URL, json={**data, "sign": sign},
        headers={'Content-Type': 'application/json'},
        timeout=TIMEOUT_TIME
    )
    if answer.status_code == 200:
        data = answer.json()['data']
        return redirect(data['url'])
    elif answer.status_code == 500:
        pass
    return