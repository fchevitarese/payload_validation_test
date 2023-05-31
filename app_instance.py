# app_instance.py
from flask import Flask
from database import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app
