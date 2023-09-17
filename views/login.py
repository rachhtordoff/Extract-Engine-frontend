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
from skeleton_login_frontend.exceptions import ApplicationError
from skeleton_login_frontend import config
from urllib.parse import urlparse
from urllib.parse import urljoin

login = Blueprint("login", __name__)


# rar
@login.route("/login")
def display_login_page():
    session["next"] = request.args.get("next", "/")
    if session.get("keep_me_logged_in_company"):
        if session["keep_me_logged_in_company"] == "logged_in":
            return redirect(
                config.COMPANY_FRONTEND_URL
                + "account-setup/"
                + str(session["account_id"])
            )
    return render_template(
        "pages/display_logins.html", error="non", CDN_URL=config.CDN_URL
    )


@login.route("/login/oauth")
def display_oauth_login_page():
    return render_template("pages/display_oauth_logins.html", CDN_URL=config.CDN_URL)


@login.route("/login/reset_pass", methods=["GET"])
def reset_pass():
    if "user_id" in session:
        session.clear()
    return render_template("pages/reset_pass.html", CDN_URL=config.CDN_URL)


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

        url = current_app.config["LOGIN_API_URL"] + "/update_pass"
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
                    error="pass-not-set",
                    login_fe=config.COMPANY_LOGIN_FRONTEND_URL,
                    CDN_URL=config.CDN_URL,
                )
            if json_data["error_code"] == "u005":
                return render_template(
                    "pages/new_pass.html",
                    error="expired",
                    login_fe=config.COMPANY_LOGIN_FRONTEND_URL,
                    CDN_URL=config.CDN_URL,
                )
            if json_data["error_code"] == "u005":
                return render_template(
                    "pages/new_pass.html",
                    error="invalid-link",
                    login_fe=config.COMPANY_LOGIN_FRONTEND_URL,
                    CDN_URL=config.CDN_URL,
                )
            if json_data['error_code'] == 'u004':
                return render_template('pages/new_pass.html', error="expired", login_fe=config.COMPANY_LOGIN_FRONTEND_URL, CDN_URL=config.CDN_URL)
            
            raise ApplicationError("something has gone wrong trying to send you an email", 'unspecified')


        return render_template("pages/display_logins.html", error="mew-pass-set")


@login.route("/login/oauthGoogleValidate", methods=["POST"])
def validate_google_token():
    post_data = request.form

    url = current_app.config["LOGIN_API_URL"] + "/verify_google_token"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    payload = {}
    payload["token"] = post_data["authorization_grant"]
    response = g.requests.request(
        "POST", url, data=json.dumps(payload), headers=headers
    )
    json_data = json.loads(response.text)

    session["account_id"] = json_data["id"]
    session["email"] = post_data["email"].lower()
    session["google_login"] = True
    session["error"] = ""
    session["payments_error"] = ""
    session["form_user"] = ""
    session["insurance_errors"] = ""

    return redirect(
        config.COMPANY_FRONTEND_URL + "account-setup/" + str(json_data["id"])
    )


@login.route("/login/validate_login", methods=["POST"])
def validate_login():
    post_data = request.form
    current_app.logger.info("validating login")
    url = current_app.config["LOGIN_API_URL"] + "/verify_login"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    payload = {}
    payload["email"] = post_data["email"].lower()
    payload["password"] = post_data["password"]
    response = g.requests.request(
        "POST", url, data=json.dumps(payload), headers=headers
    )

    json_data = json.loads(response.text)

    get_account_by_email = get_account(post_data["email"].lower())

    if response.status_code != 200:
        # code u001 has been specified to be an incorrect email and password combination so we should check for this
        if json_data["error_code"] == "u001":
            return render_template(
                "pages/display_logins.html",
                error="error-password-username",
                CDN_URL=config.CDN_URL,
            )

        raise ApplicationError(
            "something has gone wrong trying to log you in", "unspecified"
        )
    checked = "keep_me_logged_in" in request.form
    company_account = get_company_account(json_data["comp_id"])
    url = request.base_url
    url_join = urljoin(url, "/")
    print(url_join)
    if url_join[-1:] == "/":
        print(url_join[-1:])
        print(company_account[0]["url"])

        if (
            url_join[:-1] == company_account[0]["url"]
            or current_app.config["BYPASS_URL_CHECK"] == True
        ):
            if current_app.config["BYPASS_URL_CHECK"] == True:
                print("DANGER: bypassing url check for testing")
            if "keep_me_logged_in" in post_data:
                if post_data["keep_me_logged_in"] == "true":
                    session["keep_me_logged_in_company"] = "logged_in"
                    session.permanent = True

            session["account_id"] = get_account_by_email[0]["account_id"]
            session["email"] = post_data["email"].lower()
            session["cookie_policy"] = "yes"
            session["google_login"] = True
            session["error"] = ""
            session["feedback_error"] = ""
            session["form_user"] = ""
            session["payments_error"] = ""
            session["insurance_errors"] = ""
            session["staff_doc_error"] = ""
            print(session)

            return redirect(
                config.COMPANY_FRONTEND_URL
                + "account-setup/"
                + str(get_account_by_email[0]["account_id"])
            )
        return render_template(
            "pages/display_logins.html", error="error-wrong-url", CDN_URL=config.CDN_URL
        )


@login.route("/validate_register", methods=["POST"])
def validate_register():
    post_data = request.form

    # check that the two provided passwords match
    if post_data["password"] != post_data["password_verify"]:
        raise ApplicationError("your passwords did not match", "unspecified")

    url = current_app.config["LOGIN_API_URL"] + "/register_user"
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
        if json_data["error_code"] == "u002":
            return render_template(
                "pages/display_logins.html", error="email-error", CDN_URL=config.CDN_URL
            )

        raise ApplicationError(
            "something has gone wrong trying to log you in", "unspecified"
        )
    session["account_id"] = json_data["id"]
    session["email"] = post_data["email"].lower()
    session["google_login"] = True
    session["error"] = ""
    session["form_user"] = ""

    return redirect(
        config.COMPANY_FRONTEND_URL + "account-setup/" + str(json_data["id"])
    )


@login.route("/login/reset_pass", methods=["POST"])
def reset_pass_post():
    url = current_app.config["LOGIN_API_URL"] + "/reset_pass"
    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    payload = {}
    payload["email"] = request.form["email"].lower()
    payload["type"] = "reset_pass_email"

    response = g.requests.request(
        "POST", url, data=json.dumps(payload), headers=headers
    )

    json_data = json.loads(response.text)

    print(response.status_code)

    if response.status_code != 200:
        # code u001 has been specified to be an incorrect email and password combination so we should check for this
        if json_data["error_code"] == "u001":
            return render_template(
                "pages/reset_pass.html",
                error="reset-pass-not-sent",
                CDN_URL=config.CDN_URL,
            )

        raise ApplicationError(
            "something has gone wrong trying to send you an email", "unspecified"
        )

    return render_template(
        "pages/display_logins.html", error="reset-pass-sent", CDN_URL=config.CDN_URL
    )


@login.route("/logout")
def display_logout_page():
    session.clear()
    return render_template("pages/display_logout.html", CDN_URL=config.CDN_URL)


def get_company_account(id):
    resp = requests.get(config.USERS_API_URL + "/comp/" + str(id))
    data = json.loads(resp.text)
    return data


def get_account(email):
    params = {"email": email}

    headers = {
        "Content-Type": "application/json",
    }

    resp = requests.get(
        config.USERS_API_URL + "/get_company_by_email",
        data=json.dumps(params),
        headers=headers,
    )

    data = json.loads(resp.text)
    return data
