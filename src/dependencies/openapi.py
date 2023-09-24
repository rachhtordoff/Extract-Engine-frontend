from flask import (
    current_app,
    session,
    g,
)
import json

def extract_data(data):
    url = current_app.config["OPENAPI_API"] + "/chatgpt_call"

    headers = {
        "Content-type": "application/json",
        "Accept": "text/plain",
        "Authorization": f"Bearer {session.get('access_token')}"
    }

    payload = {
        'output_type':'',
        'input_type':''
    }

    response = g.requests.request(
        "POST", url, data=json.dumps(payload), headers=headers
    )

    json_data = json.loads(response.text)