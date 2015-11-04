from flask import jsonify, url_for, current_app


class ValidationError(ValueError):
    pass


def not_modified():
    response = {'status': 304, 'error': 'not modified'}
    return response


def bad_request(message):
    response = {'status': 400, 'error': 'bad request',
                'message': message}
    return response


def forbidden(message):
    response = {'status': 403, 'error': 'forbidden', 'message': message}
    return response


def not_found(message):
    response = {'status': 404, 'error': 'not found',
                'message': message}
    return response


def not_allowed():
    response = {'status': 405, 'error': 'method not allowed'}
    return response


def precondition_failed():
    response = {'status': 412, 'error': 'precondition failed'}
    return response
