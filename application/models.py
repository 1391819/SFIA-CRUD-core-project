from application import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, DateField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

#########################################################################################
# tables


class Items(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.category_id"), nullable=False
    )
    price = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    orders_items = db.relationship("OrdersItems", backref="items")


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    items = db.relationship("Items", backref="category")


class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    orders = db.relationship("Orders", backref="customer")


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.customer_id"), nullable=False
    )
    order_date = db.Column(db.DateTime, nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    orders_items = db.relationship("OrdersItems", backref="orders")


class OrdersItems(db.Model):
    orders_items_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


#########################################################################################
# custom validators
# custom validator for the email, it needs to be unique
class CustomerEmailCheck:
    def __init__(self, message=None):
        if not message:
            message = "Please choose another email"
        self.message = message

    def __call__(self, form, field):
        existing_customer = Customers.query.filter_by(email=field.data).first()
        if existing_customer:
            raise ValidationError(self.message)


# custom validator for the card number
class CardNumberCheck:
    def __init__(self, message=None):
        if not message:
            message = "Please re-enter your card number"
        self.message = message

    def __call__(self, form, field):
        # remove white spaces
        card_number = field.data.replace(" ", "")
        if not card_number.isdigit() or len(card_number) != 16:
            raise ValidationError(self.message)


# custom validator for the security code
class CardSecurityCodeCheck:
    def __init__(self, message=None):
        if not message:
            message = "Please re-enter your card's CVV/CVC code"
        self.message = message

    def __call__(self, form, field):
        security_code = field.data
        if not (100 <= security_code <= 999):
            raise ValidationError(self.message)


# custom validator for the expiry date
class CardExpiryDateCheck:
    def __init__(self, message=None):
        if not message:
            message = "Please re-enter your card's expiry date"
        self.message = message

    def __call__(self, form, field):
        expiry_date = field.data
        today = datetime.today().date()
        if expiry_date < today:
            raise ValidationError(self.message)


#########################################################################################
# forms
# shipping information form
class ShippingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            CustomerEmailCheck("This email is already registered in our system"),
        ],
    )
    address = StringField("Address", validators=[DataRequired()])
    post_code = StringField("Post code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    submit = SubmitField("Proceed to payment")


# payment details form
class PaymentForm(FlaskForm):
    cardholder_name = StringField("Cardholder Name", validators=[DataRequired()])
    card_number = StringField(
        "Card Number",
        validators=[
            DataRequired(),
            CardNumberCheck("Please enter a valid 16-digit card number"),
        ],
    )
    expiry_date = DateField(
        "Expiry Date",
        validators=[
            DataRequired(),
            CardExpiryDateCheck("The card seems to have expired"),
        ],
    )
    security_code = IntegerField(
        "CVV/CVC",
        validators=[
            DataRequired(),
            CardSecurityCodeCheck("Please enter a valid 3-digit security code"),
        ],
    )
    submit = SubmitField("Place order")
