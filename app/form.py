from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import DecimalField, TextAreaField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from app.utils import EUR_CURRENCY, USD_CURRENCY, RUB_CURRENCY


class PaymentForm(FlaskForm):
    amount = DecimalField("Цена", places=2)
    currency = SelectField(
        "currency",
        choices=[(EUR_CURRENCY, "EUR"), (USD_CURRENCY, "USD"), (RUB_CURRENCY, "RUB")],
        validate_choice=False,
        validators=[],
    )
    description = TextAreaField(
        "Описание", validators=[InputRequired(), Length(max=250)]
    )
    submit = SubmitField("Оплатить")

    def validate_amount(self, field):
        if field.data and field.data.quantize(Decimal("1.00")) < 0:
            raise ValidationError('Amount must be positive')
        if field.data.quantize(Decimal("1.00")) == 0:
            raise ValidationError('Amount can not be ziro')
