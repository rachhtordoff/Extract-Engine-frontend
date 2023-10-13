from flask_jwt_extended import decode_token, create_access_token
from flask_jwt_extended.exceptions import (
    JWTDecodeError, NoAuthorizationError,
    InvalidHeaderError, WrongTokenError,
    RevokedTokenError, FreshTokenRequired
)
from flask import redirect, session
from functools import wraps
from datetime import timedelta
from src import config
import requests


def check_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('access_token', None)
        if not token:
            return redirect('./login'), 401

        try:
            decode_token(token)
        except (NoAuthorizationError,
                JWTDecodeError,
                InvalidHeaderError,
                WrongTokenError,
                RevokedTokenError,
                FreshTokenRequired):
            refresh_token = session.get('refresh_token', None)
            if not refresh_token:
                return redirect('./login'), 401
            # If using Flask-Restful, you may want to use 'reqparse' instead of 'requests'
            url = config.USER_API_URL + "/token/refresh"
            new_token_response = requests.post(url, json={'refresh_token': refresh_token})

            if new_token_response.status_code != 200:
                return redirect('./login'), 401

            new_token = new_token_response.json().get('access_token')
            session['access_token'] = new_token

            try:
                decode_token(new_token)
            except (NoAuthorizationError,
                    JWTDecodeError,
                    InvalidHeaderError,
                    WrongTokenError,
                    RevokedTokenError,
                    FreshTokenRequired):
                return redirect('./login'), 401

        except Exception:
            return redirect('./login'), 401

        return f(*args, **kwargs)

    return decorated_function


def generate_test_jwt(testemail="test_user@gmail.com"):
    """Generate a test JWT for a given identity."""
    return create_access_token(identity=testemail, expires_delta=timedelta(days=30))
