from flask_wtf import FlaskForm
from wtforms import DecimalField, TextAreaField, SelectField, SubmitField
from wtforms.validators import (
    InputRequired, Length
)


class PaymentForm(FlaskForm):
    amount = DecimalField('Цена', places=2)
    currency = SelectField(
        'currency',
        choices=[(978, 'EUR'), (840, 'USD'), (643, 'RUB')],
        validate_choice=False,
        validators=[]
    )
    description = TextAreaField(
        'Описание',
        validators=[InputRequired(), Length(max=250)]
    )
    submit = SubmitField('Оплатить')
