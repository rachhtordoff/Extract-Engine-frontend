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
from src.utilities import jwt_util
from src.dependencies import openapi

extract = Blueprint("extract", __name__)

@extract.route("/extract")
@jwt_util.check_jwt
def extract_data():
    
    openapi.extract_data({})

    return render_template(
        "pages/dashboard-home.html"
    )

@extract.route("/extract_pdf", methods=['POST'])
@jwt_util.check_jwt
def extract_pdf():
    
    post_data = request.form
    openapi.extract_data(post_data)

    return render_template(
        "pages/dashboard-home.html"
    )