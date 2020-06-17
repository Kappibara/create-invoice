from decimal import Decimal
from http.client import HTTPException

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
        currency = int(form.currency.data)
        if currency == EUR_CURRENCY:
            return get_pay_protocol(form, payment)
        elif currency == USD_CURRENCY:
            return get_bill_protocol(form, payment)
        elif currency == RUB_CURRENCY:
            return get_invoice(form, payment)
    return render_template('form/pay_form.html', form=form)


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return render_template("errors/error.html", e=e), 500


@app.route('/<path:path>/')
def any_path(path):
    return redirect(url_for('payment'))
