from pprint import pprint

import requests
from flask import render_template

from app.utils import create_sign, SHOP_ID, RUB_CURRENCY, TIMEOUT_TIME

PIASTIX_INVOICE_URL = 'https://core.piastrix.com/invoice/create'
REQUIRED_FIELDS_INVOICE = [
    'amount', 'currency', 'payway',
    'shop_id', 'shop_order_id'
]


def get_invoice(form, payment):
    data = {
        "amount": float(form.amount.data),
        "currency": RUB_CURRENCY,
        "payway": "payeer_rub",
        "shop_id": SHOP_ID,
        "shop_order_id": payment.shop_order_id,
    }
    sign = create_sign(data, REQUIRED_FIELDS_INVOICE)
    response = requests.post(
        PIASTIX_INVOICE_URL, json={**data, "sign": sign},
        headers={'Content-Type': 'application/json'},
        timeout=TIMEOUT_TIME
    )

    if response.status_code != 200:
        raise Exception

    data = response.json()['data']
    data = {'m_curorderid': data['data']['m_curorderid'],
            'm_historyid': data['data']['m_historyid'],
            'm_historytm': data['data']['m_historytm'],
            'referer': data['data']['referer']}
    return render_template('form/invoice_form.html', **data)
