import hashlib

TIMEOUT_TIME = 5

PAY_URL = 'https://pay.piastrix.com/ru/pay'
PIASTIX_BILL_URL = 'https://core.piastrix.com/bill/create'
PIASTIX_INVOICE_URL = 'https://core.piastrix.com/invoice/create'
SHOP_ID = 5
SHOP_SECRET_KEY = 'SecretKey01'

REQUIRED_FIELDS_PAY = ['amount', 'currency', 'shop_id', 'shop_order_id']
REQUIRED_FIELDS_BILL = [
    'payer_currency', 'shop_amount',
    'shop_currency', 'shop_id', 'shop_order_id'
]
REQUIRED_FIELDS_INVOICE = [
    'amount', 'currency', 'payway',
    'shop_id', 'shop_order_id'
]


def create_sign(data, fields):
    sorted_fields = sorted(fields)
    str_for_sign = ':'.join(
        str(data[key]) for key in sorted_fields
    ) + SHOP_SECRET_KEY
    return hashlib.sha256(str_for_sign.encode()).hexdigest()