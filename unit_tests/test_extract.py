import unittest
from flask import template_rendered
from src import app
from src.utilities import jwt_util
from contextlib import contextmanager


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class ExtractTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.client = app.test_client()
        self.client.testing = True

        self.test_jwt = jwt_util.generate_test_jwt()

    def test_extract_data_route(self):
        with self.app.test_client() as client:
            with client.session_transaction() as session:
                session['access_token'] = self.test_jwt # noqa

            with captured_templates(self.app) as templates:
                response = client.get('/extract', headers={'Authorization': f'Bearer {self.test_jwt}'})
                self.assertEqual(response.status_code, 200)

                # Check if the expected template was rendered
                rendered_template_names = [template[0].name for template in templates]
                self.assertIn("pages/extract-home.html", rendered_template_names)

    def test_url_list_route(self):

        with self.client.session_transaction() as session:
            session['access_token'] = self.test_jwt # noqa

        data = {
            'phrases[]': ["test1", "test2"],
            'urls': 'https://example.com\r\nhttps://example2.com'
        }
        response = self.client.post('/url-list', data=data, headers={'Authorization': f'Bearer {self.test_jwt}'})
        self.assertEqual(response.status_code, 200)

    def test_missing_jwt(self):
        response = self.client.get('/extract')
        self.assertEqual(response.status_code, 401)
        self.assertIn("/login", response.headers.get("Location"))


if __name__ == "__main__":
    unittest.main()
