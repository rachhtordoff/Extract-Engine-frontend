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

LOGCONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"()": "src.extensions.JsonFormatter"},
        "audit": {"()": "src.extensions.JsonAuditFormatter"},
    },
    "filters": {
        "contextual": {"()": "src.extensions.ContextualFilter"}
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
