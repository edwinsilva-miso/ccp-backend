import functools
import logging

from flask import request, jsonify
from ..adapters.users_adapter import UsersAdapter


def token_required(f):
    """
    Decorator to check if a token is present in the request headers.
    Passes the token to the decorated function as a keyword argument.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logging.error("Missing Authorization header.")
            return jsonify({'msg': 'Unauthorized'}), 401

        jwt = token.split('Bearer ')[-1] if 'Bearer ' in token else token
        kwargs['jwt'] = jwt
        return f(*args, **kwargs)

    return decorated_function


def validate_token(f):
    """
    Decorator to validate if a token is present and valid using UsersAdapter.
    Passes the token to the decorated function as a keyword argument if valid.
    """

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logging.error("Missing Authorization header.")
            return jsonify({'msg': 'Unauthorized'}), 401

        adapter = UsersAdapter()
        response, status_code = adapter.get_user_info(token)
        if status_code != 200:
            logging.error("Invalid token.")
            return jsonify({'msg': 'Unauthorized'}), 401

        jwt = token.split('Bearer ')[-1] if 'Bearer ' in token else token
        kwargs['jwt'] = jwt
        return f(*args, **kwargs)

    return decorated_function
