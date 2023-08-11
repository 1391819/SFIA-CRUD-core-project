from application import app, db
from application.models import Items, Categories
from flask import render_template


@app.route("/items")
def all_items():
    items = Items.query.all()
    return render_template("items.html", items=items)
