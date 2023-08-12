from application import app, db
from application.models import Items, Categories
from flask import render_template, jsonify, redirect, url_for, request, session
import random


@app.route("/")
@app.route("/home")
def index():
    # a bit of trickery, we get random items
    total_items = Items.query.count()

    # number of items we want to retrieve
    # for now, it's pretty much the entire database
    n_items = 4

    # generating random indices for selecting random items
    random_indices = random.sample(range(1, total_items + 1), n_items)

    # we query the database for the items with the generated indices
    random_items = Items.query.filter(Items.item_id.in_(random_indices)).all()

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


@app.route("/categories")
def categories_page():
    categories = Categories.query.all()
    # adding an "all categories" option to the list of categories
    all_categories = [{"category_id": -1, "name": "All Categories"}] + categories
    return render_template("categories.html", categories=all_categories)


@app.route("/get_items_by_category/<int:category_id>")
def get_items_by_category(category_id):
    # retrive items that are part of the selected category
    items = Items.query.filter_by(category_id=category_id).all()
    # create list with all items
    items_list = [
        {
            # further fields can be added if they need to be displayed
            "item_id": items.item_id,
            "name": items.name,
            # "category": items.category.name,
            "price": items.price,
            "filename": items.filename,
        }
        for items in items
    ]
    # return JSON data so we can use it in categories_products.js
    # this is done in such a way as to not need a page reload
    # every time the user clicks on a different category
    return jsonify({"items": items_list})


@app.route("/get_all_items")
def get_all_items():
    # this function is just used to display the All Categories items in the categories page
    # might be useful for future things?
    # the all_items view function unfortunately can't be reused since it renders a particular templat
    items = Items.query.all()
    # create list with all items
    items_list = [
        {
            # further fields can be added if they need to be displayed
            "item_id": items.item_id,
            "name": items.name,
            # "category": items.category.name,
            "price": items.price,
            "filename": items.filename,
        }
        for items in items
    ]
    return jsonify({"items": items_list})


###################################################################
# cart page routes


@app.route("/add_to_cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    # get item by id
    # the reason why we re-retrieve the item instead of just passing
    # all the necessary fields is
    # 1) simplified view function
    # 2) if item data changes WHILE the user is on the site (i.e., price)
    #    the change wouldn't be reflected in what the user is seeing
    item = Items.query.filter_by(item_id=item_id).first()

    # retrieve selected quantity
    quantity = int(request.form["quantity"])

    # check if there's already a cart in session
    if "cart" not in session:
        session["cart"] = {}

    # else create it
    cart = session["cart"]

    # we cast to strings to keep data serialisable
    # if item is already in the cart, we just need to increase the quantity
    if str(item_id) in cart:
        cart[str(item_id)]["quantity"] += quantity
    else:
        # creation of "item info" dict
        # contains data which will be useful to be displayed in the cart page
        cart[str(item_id)] = {
            "name": item.name,
            "filename": item.filename,
            "price": item.price,
            "quantity": quantity,
        }

    # indicating that the session has been modified
    session.modified = True

    # redirecting to cart page
    return redirect(url_for("cart_page"))


@app.route("/cart")
def cart_page():
    # retrieving cart from session
    cart = session.get("cart", {})

    return render_template("cart_page.html", cart=cart)


@app.route("/clear_cart", methods=["POST"])
def clear_cart():
    session.pop("cart", None)
    session.modified = True
    return redirect(url_for("cart_page"))


###################################################################
# checkout


@app.route("/checkout", methods=["POST"])
def checkout():
    return f"Checkout page"
