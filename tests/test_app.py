# TODO: Separate into unit and integration testing. It's never good to have one big file. Modularity is a thing

from application import db, app
from application.models import Items, Categories, Customers, Orders, OrdersItems
from application.routes.routes import calculate_total_cart_price
from flask_testing import TestCase
from flask import url_for


# create base class
class TestBase(TestCase):
    def create_app(self):
        # pass in testing configurations for the app
        # we shouldn't use production database but testing database
        # a new one should be created (we will just use an sqlite one)

        # TODO: Check __init__.py under application to find out why this is commented
        app.config.update(
            # SQLALCHEMY_DATABASE_URI="sqlite:///testdata.sqlite",
            TESTING=True,
            WTF_CSRF_ENABLED=False,
        )

        # print(app.config["SQLALCHEMY_DATABASE_URI"]) # debug

        return app

    # this will be called before every test
    def setUp(self):
        # create tables
        db.create_all()

        # creating testing categories and products
        # a few of these might have not been used during the tests
        # TODO: Remove unused instances
        jeans_category = Categories(name="Jeans")
        skirts_category = Categories(name="Skirt")
        tshirts_category = Categories(name="T-shirt")

        jeans_item = Items(
            name="Blue Force",
            stock=999,
            category=jeans_category,
            price=9.99,
            filename="jeans_1.jpg",
        )

        jeans_item_2 = Items(
            name="Dark Force",
            stock=999,
            category=jeans_category,
            price=9.99,
            filename="jeans_2.jpg",
        )

        skirt_item = Items(
            name="Comfy White",
            stock=5,
            category=skirts_category,
            price=4.99,
            filename="skirt_1.jpg",
        )

        skirt_item_2 = Items(
            name="Formal Blue",
            stock=999,
            category=skirts_category,
            price=4.99,
            filename="skirt_2.jpg",
        )

        tshirt_item = Items(
            name="Pricess Top",
            stock=999,
            category=tshirts_category,
            price=14.99,
            filename="tshirt_1.jpg",
        )

        tshirt_item_2 = Items(
            name="Flower Garden",
            stock=999,
            category=tshirts_category,
            price=14.99,
            filename="tshirt_2.jpg",
        )

        # saving items to test db
        db.session.add_all(
            [
                jeans_category,
                skirts_category,
                tshirts_category,
                jeans_item,
                jeans_item_2,
                skirt_item,
                skirt_item_2,
                tshirt_item,
                tshirt_item_2,
            ]
        )
        db.session.commit()

    # this will be called after every test
    def tearDown(self):
        # clear all the used session variables
        with self.app.test_client() as client:
            with client.session_transaction() as session:
                if "cart" in session:
                    session.pop("cart")
                if "customer_data" in session:
                    session.pop("customer_data")

        # clear the db session and remove all contents
        db.session.remove()
        db.drop_all()


class TestViews(TestBase):
    def test_index(self):
        """Testing / and /home endpoints"""
        response = self.client.get(url_for("index"))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used("index.html")

    def test_products(self):
        """Testing /products endpoint"""
        response = self.client.get(url_for("products"))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used("items.html")

        items = Items.query.all()

        for item in items:
            self.assertIn(item.name.encode(), response.data)

    def test_product_details(self):
        """Testing /products/<int:item_id> endpoint"""
        item_id = 1
        response = self.client.get(url_for("product_details", item_id=item_id))
        self.assertEqual(response.status_code, 200)

        self.assert_template_used("product_details.html")

        sample_item = Items.query.filter_by(item_id=item_id).first()
        self.assertIn(sample_item.name.encode(), response.data)

    def test_categories(self):
        """Testing /categories endpoint"""
        response = self.client.get(url_for("categories"))
        self.assertEqual(response.status_code, 200)

        self.assert_template_used("categories.html")

        self.assertIn(b"All Categories", response.data)

        categories = Categories.query.all()
        for category in categories:
            self.assertIn(category.name.encode(), response.data)

    def test_get_products_by_category(self):
        """Testing /get_products_by_category/<int:category_id> endpoint"""
        category_id = 1
        response = self.client.get(
            url_for("get_products_by_category", category_id=category_id)
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content_type, "application/json")

        json_data = response.get_json()

        self.assertIn("items", json_data)

        items = json_data["items"]
        self.assertIsInstance(items, list)

        for item in items:
            self.assertIn("item_id", item)
            self.assertIn("name", item)
            self.assertIn("price", item)
            self.assertIn("filename", item)

    def test_get_all_items(self):
        """Testing /get_all_items endpoint"""
        response = self.client.get(url_for("get_all_items"))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content_type, "application/json")

        json_data = response.get_json()

        self.assertIn("items", json_data)

        items = json_data["items"]
        self.assertIsInstance(items, list)

        for item in items:
            self.assertIn("item_id", item)
            self.assertIn("name", item)
            self.assertIn("price", item)
            self.assertIn("filename", item)

        json_item_ids = [item["item_id"] for item in items]
        db_item_ids = [item.item_id for item in Items.query.all()]

        for item_id in db_item_ids:
            self.assertIn(item_id, json_item_ids)

    def test_cart_page(self):
        """Testing /cart endpoint"""
        sample_item_1 = Items.query.filter_by(item_id=1).first()
        sample_item_2 = Items.query.filter_by(item_id=2).first()

        sample_cart = {
            str(sample_item_1.item_id): {
                "name": sample_item_1.name,
                "filename": sample_item_1.filename,
                "price": sample_item_1.price,
                "category": sample_item_1.category.name,
                "quantity": 2,
                # "stock": sample_item_1.stock,
            },
            str(sample_item_2.item_id): {
                "name": sample_item_2.name,
                "filename": sample_item_2.filename,
                "price": sample_item_2.price,
                "category": sample_item_2.category.name,
                "quantity": 1,
                # "stock": sample_item_2.stock,
            },
        }

        with self.client.session_transaction() as sess:
            sess["cart"] = sample_cart

        response = self.client.get(url_for("cart_page"))
        self.assertEqual(response.status_code, 200)

        for item_id, item_info in sample_cart.items():
            for key, value in item_info.items():
                if key in ("name", "filename", "category"):
                    self.assertIn(value.encode(), response.data)
                else:
                    self.assertIn(str(value).encode(), response.data)

        expected_total_price = calculate_total_cart_price(sample_cart)
        self.assertIn(str(expected_total_price).encode(), response.data)

    def test_add_to_cart_new_item(self):
        """Testing /add_to_cart/<int:item_id> endpoint: new item"""
        sample_item = Items.query.filter_by(item_id=1).first()

        response = self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            cart = sess["cart"]
            self.assertIsNotNone(cart)
            self.assertTrue(str(sample_item.item_id) in cart)
            self.assertEqual(cart[str(sample_item.item_id)]["quantity"], 2)

        self.assert_template_used("cart_page.html")

    def test_add_to_cart_existing_item(self):
        """Testing /add_to_cart/<int:item_id> endpoint: existing item"""
        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        response = self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            cart = sess["cart"]
            self.assertIsNotNone(cart)
            self.assertTrue(str(sample_item.item_id) in cart)
            self.assertEqual(cart[str(sample_item.item_id)]["quantity"], 4)

        self.assert_template_used("cart_page.html")

    def test_remove_from_cart_item_removed(self):
        """Testing successfull /remove_from_cart/<int:item_id> endpoint"""
        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        response = self.client.post(
            url_for("remove_from_cart", item_id=sample_item.item_id),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            cart = sess["cart"]
            self.assertFalse(str(sample_item.item_id) in cart)

        self.assertEqual(response.content_type, "application/json")

        response_json = response.json

        self.assertEqual(
            response_json,
            {"message": "Item removed from the cart successfully", "cart_length": 0},
        )

    def test_remove_from_cart_item_not_found(self):
        """Testing unsuccessfull /remove_from_cart/<int:item_id> endpoint"""
        sample_item = Items.query.filter_by(item_id=1).first()

        response = self.client.post(
            url_for("remove_from_cart", item_id=sample_item.item_id),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Item not found in the cart", response.data)

    def test_decrease_quantity_item_found(self):
        """Testing successfull /decrease_quantity/<int:item_id> endpoint"""
        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        response = self.client.post(
            url_for("decrease_quantity", item_id=sample_item.item_id),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            cart = sess["cart"]
            updated_quantity = cart[str(sample_item.item_id)]["quantity"]
            updated_total_price = calculate_total_cart_price(cart)
            self.assertEqual(updated_quantity, 1)

        self.assertEqual(response.content_type, "application/json")

        response_json = response.json
        self.assertEqual(
            response_json["message"], "Item quantity decreased successfully"
        )
        self.assertEqual(response_json["updated_quantity"], 1)

        self.assertEqual(response_json["updated_total_price"], updated_total_price)

    def test_decrease_quantity_item_not_found(self):
        """Testing successfull /decrease_quantity/<int:item_id> endpoint"""
        sample_item = Items.query.filter_by(item_id=1).first()

        response = self.client.post(
            url_for("decrease_quantity", item_id=sample_item.item_id),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Item not found in the cart", response.data)

    def test_increase_quantity_item_found(self):
        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        response = self.client.post(
            url_for("increase_quantity", item_id=sample_item.item_id),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            cart = sess["cart"]
            updated_quantity = cart[str(sample_item.item_id)]["quantity"]
            updated_total_price = calculate_total_cart_price(cart)
            self.assertEqual(updated_quantity, 3)

        self.assertEqual(response.content_type, "application/json")

        response_json = response.json
        self.assertEqual(
            response_json["message"], "Item quantity increased successfully"
        )
        self.assertEqual(response_json["updated_quantity"], 3)

        self.assertEqual(response_json["updated_total_price"], updated_total_price)

    def test_increase_quantity_item_not_found(self):
        """Testing successfull /increase_quantity/<int:item_id> endpoint"""
        sample_item = Items.query.filter_by(item_id=1).first()

        response = self.client.post(
            url_for("increase_quantity", item_id=sample_item.item_id),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Item not found in the cart", response.data)

    def test_checkout_get(self):
        response = self.client.get(url_for("checkout"))

        # redirect expected since there is no cart
        self.assertEqual(response.status_code, 302)

        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        response = self.client.get(url_for("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used("checkout.html")

    def test_payment_get(self):
        response = self.client.get(url_for("payment"))

        # redirect expected since there is no customer data
        self.assertEqual(response.status_code, 302)

        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        customer_form_data = {
            "name": "Roberto Nacu",
            "email": "rnacu@example.com",
            "address": "123 Way",
            "post_code": "NE2 8AS",
            "country": "UK",
        }

        self.client.post(
            url_for("checkout"), data=customer_form_data, follow_redirects=True
        )

        response = self.client.get(url_for("payment"))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used("payment.html")

    def test_process_order(self):
        # Simulate adding items to cart and going through the checkout process
        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        customer_form_data = {
            "name": "Roberto Nacu",
            "email": "test@example.com",
            "address": "123 Way",
            "post_code": "NE2 8AS",
            "country": "UK",
        }

        self.client.post(
            url_for("checkout"), data=customer_form_data, follow_redirects=True
        )

        payment_form_data = {
            "cardholder_name": "Roberto Nacu",
            "card_number": "1234567812345678",
            "expiry_date": "2023-12-11",
            "security_code": "123",
        }

        self.client.post(
            url_for("payment"), data=payment_form_data, follow_redirects=True
        )

        response = self.client.get(url_for("process_order"))
        # redirect since on page reload the user will be redirected to checkout if there is no customer data
        # and there won't be since the customer_data session var is popped
        self.assertEqual(response.status_code, 302)
        self.assert_template_used("process_order.html")


class TestCRUD(TestBase):
    def test_checkout_form_post(self):
        sample_item = Items.query.filter_by(item_id=1).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        customer_form_data = {
            "name": "Roberto Nacu",
            "email": "rnacu@example.com",
            "address": "123 Way",
            "post_code": "NE2 8AS",
            "country": "UK",
        }

        response = self.client.post(
            url_for("checkout"), data=customer_form_data, follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assert_template_used("payment.html")

        with self.client.session_transaction() as sess:
            customer_data = sess["customer_data"]
            self.assertEqual(customer_data, customer_form_data)

        obj1 = Customers.query.filter_by(email=customer_form_data["email"]).first()
        assert obj1 is not None
        self.assertEqual(obj1.email, "rnacu@example.com")

    def test_payment_form_post(self):
        sample_item = Items.query.filter_by(item_id=1).first()
        sample_item_2 = Items.query.filter_by(item_id=2).first()

        self.client.post(
            url_for("add_to_cart", item_id=sample_item.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        self.client.post(
            url_for("add_to_cart", item_id=sample_item_2.item_id),
            data={"quantity": 2},
            follow_redirects=True,
        )

        customer_form_data = {
            "name": "Roberto Nacu",
            "email": "rnacu@example.com",
            "address": "123 Way",
            "post_code": "NE2 8AS",
            "country": "UK",
        }

        self.client.post(
            url_for("checkout"), data=customer_form_data, follow_redirects=True
        )

        payment_form_data = {
            "cardholder_name": "Roberto Nacu",
            "card_number": "1234567812345678",
            "expiry_date": "2023-12-11",
            "security_code": "123",
        }

        response = self.client.post(
            url_for("payment"), data=payment_form_data, follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assert_template_used("process_order.html")

        customer = Customers.query.filter_by(email=customer_form_data["email"]).first()
        shipping_address = f"{customer_form_data['address']}, {customer_form_data['post_code']}, {customer_form_data['country']}"

        order = Orders.query.filter_by(customer=customer).first()
        assert order is not None
        self.assertEqual(order.shipping_address, shipping_address)

        orders_items = OrdersItems.query.filter_by(orders=order).all()
        assert orders_items is not None

        cart_item_ids = [sample_item.item_id, sample_item_2.item_id]
        for orders_item in orders_items:
            self.assertIn(orders_item.items.item_id, cart_item_ids)

        # TODO: Add assertion on multiple orders with the same item
