""" __init__.py """
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import config


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name):
    """ Application Factory """
    # instantiate the app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # set up the extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from app.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
