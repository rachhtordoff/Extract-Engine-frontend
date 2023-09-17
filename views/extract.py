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

extract = Blueprint("extract", __name__)

@extract.route("/extract")
def extract_data():
    return ''