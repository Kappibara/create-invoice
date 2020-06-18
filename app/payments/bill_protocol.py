from flask import redirect

from app.utils import USD_CURRENCY, SHOP_ID, get_data

PIASTIX_BILL_URL = "https://core.piastrix.com/bill/create"

REQUIRED_FIELDS_BILL = [
    "payer_currency",
    "shop_amount",
    "shop_currency",
    "shop_id",
    "shop_order_id",
]


def get_bill_protocol(form, payment):
    data = {
        "payer_currency": USD_CURRENCY,
        "shop_amount": float(form.amount.data),
        "shop_currency": USD_CURRENCY,
        "shop_id": SHOP_ID,
        "shop_order_id": str(payment.shop_order_id),
    }

    data = get_data(data, REQUIRED_FIELDS_BILL, PIASTIX_BILL_URL)
    return redirect(data["url"])
