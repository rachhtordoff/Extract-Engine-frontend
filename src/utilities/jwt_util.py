from flask_jwt_extended import decode_token, create_access_token
from src import jwt
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError, InvalidHeaderError, WrongTokenError, RevokedTokenError, FreshTokenRequired
from flask import (
    redirect,
    session,
)
from functools import wraps
from datetime import timedelta

def check_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('access_token', None)
        if not token:
            return redirect('./login'), 401

        try:
            decode_token(token)
        except (NoAuthorizationError, JWTDecodeError, InvalidHeaderError, WrongTokenError, RevokedTokenError, FreshTokenRequired) as e:
            return redirect('./login'), 401

        return f(*args, **kwargs)
    
    return decorated_function

def generate_test_jwt(testemail="test_user@gmail.com"):
    """Generate a test JWT for a given identity."""
    return create_access_token(identity=testemail, expires_delta=timedelta(days=30))
