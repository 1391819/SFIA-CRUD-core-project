from application import app, db
from application.models import Items, Categories
from flask import render_template
import random


@app.route("/")
@app.route("/home")
def index():
    # a bit of trickery, we get random items
    total_items = Items.query.count()

    # number of items we want to retrieve
    # for now, it's pretty much the entire database
    n_items = 5

    # generating random indices for selecting random items
    random_indices = random.sample(range(1, total_items + 1), n_items)

    # we query the database for the items with the generated indices
    random_items = Items.query.filter(Items.item_id.in_(random_indices)).all()

    print(random_items)

    # rendering appropriate template
    return render_template("index.html", items=random_items)


@app.route("/items")
def all_items():
    """Items endpoint: displaying all items

    Returns:
        _type_: _description_
    """
    # retrieving all items
    items = Items.query.all()
    # rendering appropriate template
    return render_template("items.html", items=items)


@app.route("/items/<int:item_id>")
def item_page(item_id: int):
    """Single item endpoint

    Args:
        item_id (int): ID of the item we want to display

    Returns:
        _type_: _description_
    """
    # retrieving item using passed item_id
    item = Items.query.filter_by(item_id=item_id).first()
    # rendering appropriate template
    return render_template("item_page.html", item=item)
