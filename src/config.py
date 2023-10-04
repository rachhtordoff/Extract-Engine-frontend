import os


def convert_to_bool(value):
    if value == "True":
        return True
    elif value == "False":
        return False


ALLOW_HTTPS_TRAFFIC_ONLY = convert_to_bool(
    os.environ.get("ALLOW_HTTPS_TRAFFIC_ONLY", "True")
)
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
SECRET_KEY = os.environ["SECRET_KEY"]
FLASK_LOG_LEVEL = os.environ["FLASK_LOG_LEVEL"]
USER_API_URL = os.environ["user_api_url"]
OPENAPI_API = os.environ["openapi_api_url"]
EMAIL_API_URL = os.environ["email_api_url"]
LOGIN_URL = os.environ["LOGIN_URL"]
APP_NAME = os.environ["APP_NAME"]
