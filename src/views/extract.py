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
from flask_jwt_extended import JWTManager, decode_token
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError, InvalidHeaderError, WrongTokenError, RevokedTokenError, FreshTokenRequired


extract = Blueprint("extract", __name__)

@extract.route("/extract")
def extract_data():
    
    url = current_app.config["OPENAPI_API"] + "/chatgpt_call"

    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain",
        "Authorization": f"Bearer {session.get('access_token')}"
    }

    payload = {}

    response = g.requests.request(
        "POST", url, data=json.dumps(payload), headers=headers
    )

    json_data = json.loads(response.text)


    return render_template(
        "pages/dashboard-home.html"
    )

def check_jwt():
    token = session.get('access_token', None)

    if not token:
        return redirect(url_for('login'))

    try:
        decode_token(token)
    except (NoAuthorizationError, JWTDecodeError, InvalidHeaderError, WrongTokenError, RevokedTokenError, FreshTokenRequired) as e:
        return redirect(url_for('login'))