from decimal import Decimal

import requests
from flask import redirect, url_for, make_response
from flask import render_template, request

from app import app, db
from app.form import PaymentForm
from app.models import PaymentModel
from app.utils import (
    SHOP_ID, create_sign, REQUIRED_FIELDS_PAY,
    PIASTIX_BILL_URL, REQUIRED_FIELDS_BILL, REQUIRED_FIELDS_INVOICE,
    PIASTIX_INVOICE_URL, TIMEOUT_TIME
)


@app.route('/')
def index():
    return redirect(url_for('payment'))


@app.route('/payment', methods=['GET', 'POST'])
def payment():

    form = PaymentForm()
    if form.validate_on_submit():
        amount = form.amount.data.quantize(Decimal('1.00'))
        payment = PaymentModel(
            amount=amount,
            currency=form.currency.data,
            description=form.description.data
        )
        db.session.add(payment)
        db.session.commit()

        if int(form.currency.data) == 978:
            data = {
                'amount': amount.to_eng_string(),
                'currency': form.currency.data,
                'shop_id': SHOP_ID,
                'description': form.description.data,
                'shop_order_id': payment.id
            }
            return render_template(
                'form/base_pay_form.html',
                **data,
                sign=create_sign(data, REQUIRED_FIELDS_PAY)
            )
        elif int(form.currency.data) == 840:
            data = {
                "payer_currency": 840,
                "shop_amount": float(form.amount.data),
                "shop_currency": 840,
                "shop_id": SHOP_ID,
                "shop_order_id": payment.id,
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
        elif int(form.currency.data) == 643:
            data = {
                "amount": float(form.amount.data),
                "currency": 643,
                "payway": "payeer_rub",
                "shop_id": SHOP_ID,
                "shop_order_id": payment.id,
            }
            sign = create_sign(data, REQUIRED_FIELDS_INVOICE)

            answer = requests.post(
                PIASTIX_INVOICE_URL, json={**data, "sign": sign},
                headers={'Content-Type': 'application/json'},
                timeout=TIMEOUT_TIME
            )
            if answer.status_code == 200:
                data = answer.json()['data']
                data = {'m_curorderid': data['data']['m_curorderid'],
                        'm_historyid': data['data']['m_historyid'],
                        'm_historytm': data['data']['m_historytm'],
                        'referer': data['data']['referer']}
                return render_template('form/invoice_form.html', **data)
    return render_template('form/pay_form.html', form=form)

