from flask import Flask, g, request
import uuid
import requests
from flask_jwt_extended import JWTManager
from src import config

app = Flask(__name__)
app.config.from_pyfile("config.py")

app.config['JWT_SECRET_KEY'] =  config.JWT_SECRET_KEY
jwt = JWTManager(app)


@app.before_request
def before_request():
    # Sets the transaction trace id into the global object if it has been provided in the HTTP header from the caller.
    # Generate a new one if it has not. We will use this in log messages.
    g.trace_id = request.headers.get('X-Trace-ID', uuid.uuid4().hex)
    # We also create a session-level requests object for the app to use with the header pre-set, so other APIs will
    # receive it. These lines can be removed if the app will not make requests to other LR APIs!
    g.requests = requests.Session()
    g.requests.headers.update({'X-Trace-ID': g.trace_id})


@app.after_request
def after_request(response):
    # Add the API version (as in the interface spec, not the app) to the header. Semantic versioning applies - see the
    # API manual. A major version update will need to go in the URL. All changes should be documented though, for
    # reusing teams to take advantage of.
    response.headers["X-API-Version"] = "1.0.0"
    if app.config['ALLOW_HTTPS_TRAFFIC_ONLY']:
        response.headers['Strict-Transport-Security'] = "max-age=31536000"
    return response
#these imports must be included after the app object has been created as it is imported in them
from src.blueprints import register_blueprints
from src.exceptions import register_exception_handlers

from src.extensions import register_extensions

# Register any extensions we use into the app
register_extensions(app)
register_exception_handlers(app)
register_blueprints(app)
