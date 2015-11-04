import os
from flask import Flask
from .models import db
from .auth import auth
from .errors import not_found, not_allowed
from config import config
from flask.ext.api import FlaskAPI, status, exceptions


def create_app(config_name):
    app = FlaskAPI(__name__)

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)

    from api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
