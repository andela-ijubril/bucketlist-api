from ..models import User
from flask import request, jsonify, g
from ..errors import bad_request, forbidden
from ..decorators import json
from . import api
from ..auth import verify_password


@api.route('/register/', methods=['POST'])
def create_user():

    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    details = [email, username, password]

    if not all(details):
        return bad_request("you must supply email, username and password")
    if User.query.filter_by(email=email).first() is not None and User.query.filter_by(username=username) is not None:
        return forbidden("email or username already exist")

    user = User(email=email, username=username)
    user.hash_password(password)
    user.save()

    return jsonify({'username': user.username})


@api.before_request
@api.route('/login/', methods=['POST'])
def login():

    username = request.json.get('username')
    password = request.json.get('password')

    if verify_password(username, password):
        token = g.user.generate_auth_token()
        status = "token generated successfully"
    else:
        status = "Invalid username or password"
        token = None

    return jsonify({'status': status,
                    'token': token})


@api.route('/users/')
def get_all_users():
    users = User.query.all()
    return jsonify({
        'users': users
    })
