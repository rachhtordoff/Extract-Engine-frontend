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
from src.exceptions import ApplicationError
from src import config
from urllib.parse import urlparse
from urllib.parse import urljoin

login = Blueprint("login", __name__)

@login.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        url = current_app.config["users_api_url"] + "/register"

        payload = {}
        payload["email"] = request.form['email'].lower()
        payload["password"] = request.form['password']

        response = g.requests.request(
            "POST", url, data=json.dumps(payload), headers=headers
        )

        json_data = json.loads(response.text)
        return jsonify(json_data)

        if json_data.get('message') == 'email taken':
            return render_template(
                "pages/login.html", error="email-taken"
            ) 
        else:
            return redirect(url_for('login'))
    return render_template('pages/register.html')


@login.route("/login", methods=["POST"])
def validate_login():
    post_data = request.form

    url = current_app.config["users_api_url"] + "/login"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    payload = {}
    payload["email"] = post_data["email"].lower()
    payload["password"] = post_data["password"]
    response = g.requests.request(
        "POST", url, data=json.dumps(payload), headers=headers
    )

    json_data = json.loads(response.text)

    if response.status_code != 200:
        # code u001 has been specified to be an incorrect email and password combination so we should check for this
        if json_data["error_code"] == "u001":
            return render_template(
                "pages/login.html",
                error="error-password-username"
            )

        session['username'] = json_data['username']
        session['userToken'] = json_data['userToken']
        session['refreshToken'] = json_data['refreshToken']
        session['id'] = json_data['id']
            
        if "keep_me_logged_in" in post_data:
            if post_data["keep_me_logged_in"] == "true":
                session["keep_me_logged_in"] = "logged_in"
                session.permanent = True

        session["cookie_policy"] = "yes"
        session["error"] = ""
        return redirect('./dashboard')
    
    return render_template(
        "pages/login.html", error="error-password-username"
    )

@login.route('/')
@login.route("/login")
def display_login_page():
    session["next"] = request.args.get("next", "/")
    if session.get("keep_me_logged_in"):
        if session["keep_me_logged_in"] == "logged_in":
            if not 'userToken' in session:
                return render_template(
                    "pages/login.html", error="jwt-not-in-session"
                )
            return redirect(url_for('dashboard'))

    return render_template(
        "pages/login.html"
    )


@login.route("/login/new_pass/<email>/<random>", methods=["GET", "POST"])
def set_new_pass(email, random):
    get_email = email.lower()
    get_random = random
    if request.method == "GET":
        return render_template(
            "pages/new_pass.html",
            email=get_email,
            random=get_random,
            login_fe=config.COMPANY_LOGIN_FRONTEND_URL,
            CDN_URL=config.CDN_URL,
        )
    if request.method == "POST":
        if get_random == " ":
            return render_template(
                "pages/new_pass.html",
                error="invalid-link",
                login_fe=config.CLIENT_LOGIN_FRONTEND_URL,
                CDN_URL=config.CDN_URL,
            )

        url = current_app.config["users_api_url"] + "/update_pass"
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        payload = {}
        payload["password"] = request.form["password"]
        payload["email"] = get_email.lower()
        payload["code"] = get_random

        response = g.requests.request(
            "POST", url, data=json.dumps(payload), headers=headers
        )

        json_data = json.loads(response.text)            
        if response.status_code != 200:
            # code u001 has been specified to be an incorrect email and password combination so we should check for this
            if json_data["error_code"] == "u001":
                return render_template(
                    "pages/new_pass.html",
                    error="pass-not-set"
                )
            if json_data["error_code"] == "u005":
                return render_template(
                    "pages/new_pass.html",
                    error="expired"
                )
            if json_data['error_code'] == 'u004':
                return render_template('pages/new_pass.html', error="expired")

        return render_template("pages/login.html", error="mew-pass-set")


@login.route('/protected')
def protected():
    token = session.get('jwt')
    if not token:
        return redirect(url_for('login'))
    return f'Hello, you are in a protected route! JWT: {token}'
