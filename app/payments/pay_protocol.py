from decimal import Decimal

from flask import render_template

from app.utils import SHOP_ID, create_sign

PAY_URL = 'https://pay.piastrix.com/ru/pay'
REQUIRED_FIELDS_PAY = ['amount', 'currency', 'shop_id', 'shop_order_id']


def get_pay_protocol(form, payment):
    data = {
        'amount': form.amount.quantize(Decimal('1.00')).to_eng_string(),
        'currency': form.currency.data,
        'shop_id': SHOP_ID,
        'description': form.description.data,
        'shop_order_id': payment.shop_order_id
    }
    return render_template(
        'form/base_pay_form.html',
        **data,
        sign=create_sign(data, REQUIRED_FIELDS_PAY)
    )