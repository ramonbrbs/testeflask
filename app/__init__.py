from flask import Flask
from flask_mongoengine import MongoEngine

mongo = MongoEngine()

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    mongo.init_app(app)

    from .transaction import create_module as transaction_create_module
    transaction_create_module(app)

    return app