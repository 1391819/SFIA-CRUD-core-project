from application import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, ValidationError


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


# custom validators
# custom validator for the email, it needs to be unique
def unique_email(form, field):
    email = field.data
    existing_customer = Customers.query.filter_by(email=email).first()
    if existing_customer:
        raise ValidationError("This email is already associated with an account")


# forms
# shipping information form
class ShippingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), unique_email])
    address = StringField("Address", validators=[DataRequired()])
    post_code = StringField("Post code", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    submit = SubmitField("Proceed to payment")
