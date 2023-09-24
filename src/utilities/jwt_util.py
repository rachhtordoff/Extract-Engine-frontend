from flask_jwt_extended import decode_token
from src import jwt
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError, InvalidHeaderError, WrongTokenError, RevokedTokenError, FreshTokenRequired
from flask import (
    redirect,
    session,
)
from functools import wraps

def check_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('access_token', None)
        if not token:
            return redirect('./login')

        try:
            decode_token(token)
        except (NoAuthorizationError, JWTDecodeError, InvalidHeaderError, WrongTokenError, RevokedTokenError, FreshTokenRequired) as e:
            return redirect('./login')

        return f(*args, **kwargs)
    
    return decorated_function
