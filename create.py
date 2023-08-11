from application import app, db
from application.models import *

# create the database schema or even just test db connection
with app.app_context():
    db.create_all()
