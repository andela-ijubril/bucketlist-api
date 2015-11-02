__author__ = 'Jubril'
from flask import Blueprint, g, url_for
from ..auth import auth

api = Blueprint('api', __name__)

from . import users, bucketlists, items



# @api.before_request
# @auth.login_required
# def before_request():
#     pass
