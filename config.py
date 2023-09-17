import os


def convert_to_bool(value):
    if value == "True":
        return True
    elif value == "False":
        return False


APM_ENABLED = convert_to_bool(os.environ["APM_ENABLED"])
ALLOW_HTTPS_TRAFFIC_ONLY = convert_to_bool(
    os.environ.get("ALLOW_HTTPS_TRAFFIC_ONLY", "True")
)


APP_NAME = os.environ["APP_NAME"]
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
LOGIN_API_URL = os.environ["LOGIN_API_URL"]
CDN_URL = os.environ["CDN_URL"]

COMPANY_FRONTEND_URL = os.environ["COMPANY_FRONTEND_URL"]
COMPANY_LOGIN_FRONTEND_URL = os.environ["COMPANY_LOGIN_FRONTEND_URL"]

SECRET_KEY = os.environ["SECRET_KEY"]
password_photo = os.environ["password_photo"]
reset_photo = os.environ["reset_photo"]
login_photo = os.environ["login_photo"]

SESSION_COOKIE_SECURE = convert_to_bool(os.environ["SESSION_COOKIE_SECURE"])
REMEMBER_COOKIE_SECURE = convert_to_bool(os.environ["REMEMBER_COOKIE_SECURE"])
logo = ""
# For logging
FLASK_LOG_LEVEL = os.environ["FLASK_LOG_LEVEL"]
USERS_API_URL = os.environ["USERS_API_URL"]

AUDIT_API_URL = os.environ["AUDIT_API_URL"]

# for testing
BYPASS_URL_CHECK = convert_to_bool(os.environ.get("BYPASS_URL_CHECK", "False"))

LOGCONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"()": "skeleton_login_frontend.extensions.JsonFormatter"},
        "audit": {"()": "skeleton_login_frontend.extensions.JsonAuditFormatter"},
    },
    "filters": {
        "contextual": {"()": "skeleton_login_frontend.extensions.ContextualFilter"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["contextual"],
            "stream": "ext://sys.stdout",
        },
        "audit_console": {
            "class": "logging.StreamHandler",
            "formatter": "audit",
            "filters": ["contextual"],
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "application": {"handlers": ["console"], "level": FLASK_LOG_LEVEL},
        "audit": {"handlers": ["audit_console"], "level": "INFO"},
    },
}
