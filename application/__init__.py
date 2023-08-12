from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import timedelta

# creating flask instance
app = Flask(__name__)

# creating SQLAlchemy connection

# loading environment variables
load_dotenv()

# retrieving environment variables from .env file
DB_TYPE = os.getenv("DB_TYPE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# stand-alone database - MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = (
    DB_TYPE + DB_USER + DB_PASSWORD + DB_HOST + DB_NAME
)

# form security
SECRET_KEY = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY

# setting session expiry time for security reasons
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=5)


# this is creating a simulation of the database as an object in our application
db = SQLAlchemy(app)

from application.routes import routes
