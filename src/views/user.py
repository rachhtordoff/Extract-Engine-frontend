from flask import Blueprint

user = Blueprint("user", __name__)


@user.route("/user")
def user_data():
    return ''
