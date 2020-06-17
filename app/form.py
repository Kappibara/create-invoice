from flask_wtf import FlaskForm
from wtforms import DecimalField, TextAreaField, SelectField, SubmitField
from wtforms.validators import (
    InputRequired, Length
)


from app.utils import EUR_CURRENCY, USD_CURRENCY, RUB_CURRENCY


class PaymentForm(FlaskForm):
    amount = DecimalField('Цена', places=2)
    currency = SelectField(
        'currency',
        choices=[(EUR_CURRENCY, 'EUR'), (USD_CURRENCY, 'USD'), (RUB_CURRENCY, 'RUB')],
        validate_choice=False,
        validators=[]
    )
    description = TextAreaField(
        'Описание',
        validators=[InputRequired(), Length(max=250)]
    )
    submit = SubmitField('Оплатить')
