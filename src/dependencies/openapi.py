from flask import (
    current_app,
    session,
    g,
)
import json

def extract_data_from_bank_statement(data):
    url = current_app.config["OPENAPI_API"] + "/extract_data_bank_statement"

    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain",
        "Authorization": f"Bearer {session.get('access_token')}"
    }

    response = g.requests.request(
        "POST", url, data=json.dumps(data), headers=headers
    )

    json_data = json.loads(response.text)


def extract_data_from_webscraped_urls(data):
    url = current_app.config["OPENAPI_API"] + "/extract_data_from_webscraped_urls"

    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain",
        "Authorization": f"Bearer {session.get('access_token')}"
    }

    response = g.requests.request(
        "POST", url, data=json.dumps(data), headers=headers
    )

    json_data = json.loads(response.text)