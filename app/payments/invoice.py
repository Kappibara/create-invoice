from flask import render_template

from app.utils import SHOP_ID, RUB_CURRENCY, get_data

PIASTIX_INVOICE_URL = "https://core.piastrix.com/invoice/create"
REQUIRED_FIELDS_INVOICE = ["amount", "currency", "payway", "shop_id", "shop_order_id"]


def get_invoice(form, payment):
    data = {
        "amount": float(form.amount.data),
        "currency": RUB_CURRENCY,
        "payway": "payeer_rub",
        "shop_id": SHOP_ID,
        "shop_order_id": str(payment.shop_order_id),
    }

    data = get_data(data, REQUIRED_FIELDS_INVOICE, PIASTIX_INVOICE_URL)
    if not data:
        raise Exception
    data = {
        "m_curorderid": data["data"]["m_curorderid"],
        "m_historyid": data["data"]["m_historyid"],
        "m_historytm": data["data"]["m_historytm"],
        "referer": data["data"]["referer"],
    }
    return render_template("form/invoice_form.html", **data)
