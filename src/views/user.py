from flask import (
    redirect,
    Blueprint,
    render_template,
    request,
    current_app,
    jsonify,
    session,
    g,
)
import requests
import json
from urllib.parse import urlparse
from urllib.parse import urljoin

user = Blueprint("user", __name__)

@user.route("/user")
def user_data():
    return ''