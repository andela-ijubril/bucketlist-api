from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
from .models import User
# from .errors import unauthorized

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
    # if current_app.config['USE_TOKEN_AUTH']:
    #     # token authentication
    #     g.user = User.verify_auth_token(username_or_token)
    #     return g.user is not None
    # else:
    #     # username/password authentication
    #     g.user = User.query.filter_by(username=username_or_token).first()
    #     return g.user is not None and g.user.verify_password(password)


# @auth.error_handler
# def unauthorized_error():
#     return unauthorized()
