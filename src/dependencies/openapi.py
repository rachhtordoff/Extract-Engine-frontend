from flask import (
    current_app,
    session,
    g,
)
import json


class DataExtractor:

    def __init__(self):
        self.base_url = current_app.config["OPENAPI_API"]
        self.headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {session.get('access_token')}"
        }

    def _make_post_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = g.requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return json.loads(response.text)

    def extract_data_from_bank_statement(self, data):
        endpoint = "extract_data_bank_statement"
        return self._make_post_request(endpoint, data)

    def extract_data_from_webscraped_urls(self, data):
        endpoint = "extract_data_from_webscraped_urls"
        return self._make_post_request(endpoint, data)
