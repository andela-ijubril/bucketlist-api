from flask import Blueprint, g, url_for

api = Blueprint('api', __name__)

from . import users, bucketlists, items



# @api.before_request
# @auth.login_required
# def before_request():
#     pass
