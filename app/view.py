from decimal import Decimal

from flask import redirect, url_for
from flask import render_template

from app import app, db
from app.form import PaymentForm
from app.models import PaymentModel
from app.payments.bill_protocol import get_bill_protocol
from app.payments.invoice import get_invoice
from app.payments.pay_protocol import get_pay_protocol
from app.utils import (
    EUR_CURRENCY,
    RUB_CURRENCY, USD_CURRENCY
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

        if int(form.currency.data) == EUR_CURRENCY:
            return get_pay_protocol(form, payment)
        elif int(form.currency.data) == USD_CURRENCY:
            get_bill_protocol(form, payment)
        elif int(form.currency.data) == RUB_CURRENCY:
            get_invoice(form, payment)
    return render_template('form/pay_form.html', form=form)


@app.route('/<path:path>')
def any_path():
    return redirect(url_for('payment'))

