from application import db


class Items:
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.category_id"), nullable=False
    )
    price = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    orders_items = db.relationship("OrdersItems", backref="items")


class Categories:
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    items = db.relationship("Items", backref="category")


class Customers:
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    orders = db.relationship("Orders", backref="customer")


class Orders:
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.customer_id"), nullable=False
    )
    order_date = db.Column(db.DateTime, nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    orders_items = db.relationship("OrdersItems", backref="orders")


class OrdersItems:
    orders_items_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
