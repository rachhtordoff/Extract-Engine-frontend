import unittest
from unittest.mock import patch, Mock
from flask import session
from src import app
import json

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('requests.request')
    def test_register_page_post_email_taken(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({"message": "email taken"})
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
        response = self.app.post('/register', data=payload)

        self.assertIn(b'email-taken', response.data)

    @patch('requests.request')
    def test_register_page_post_success(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }
        response = self.app.post('/register', data=payload)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    @patch('requests.request')
    def test_reset_pass_post_email_error(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({"error_code": "u001"})
        mock_response.status_code = 400
        mock_request.return_value = mock_response

        response = self.app.post('/reset_pass', data={"email": "noemail@example.com"})

        self.assertIn(b'reset-pass-not-sent', response.data)


    @patch('requests.request')
    def test_reset_pass_post_email_success(self, mock_request):
        # Mocking a successful response from the EMAIL_API_URL
        mock_response = Mock()
        mock_response.text = json.dumps({"message": "Email sent"})
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        # Mocking a successful response from the USER_API_URL (updating the user with the reset code)
        mock_response_2 = Mock()
        mock_response_2.text = json.dumps({"message": "User updated"})
        mock_response_2.status_code = 200

        mock_request.side_effect = [mock_response, mock_response_2]

        response = self.app.post('/reset_pass', data={"email": "existingemail@example.com"})

        self.assertIn(b'reset-pass-sent', response.data)

    @patch('requests.request')
    def test_reset_pass_post_email_send_fail(self, mock_request):
        # Mocking a non u001 error from the EMAIL_API_URL
        mock_response = Mock()
        mock_response.text = json.dumps({"error_code": "u002", "message": "Unknown error"})
        mock_response.status_code = 400
        mock_request.return_value = mock_response

        response = self.app.post('/reset_pass', data={"email": "existingemail@example.com"})

        self.assertNotIn(b'reset-pass-not-sent', response.data)

    @patch('requests.request')
    def test_set_new_pass_invalid_code(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({"message": "Invalid code"})
        mock_response.status_code = 400
        mock_request.return_value = mock_response

        response = self.app.post('/new_pass/existingemail@example.com/invalidcode', data={"password": "newpassword"})

        self.assertIn(b'invalid-code', response.data)

    @patch('requests.request')
    def test_validate_login_invalid_credentials(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({"message": "Invalid credentials"})
        mock_response.status_code = 400
        mock_request.return_value = mock_response

        payload = {
            "email": "john@example.com",
            "password": "wrongpassword"
        }
        response = self.app.post('/login', data=payload)

        self.assertIn(b'error-password-username', response.data)


    @patch('requests.request')
    def test_validate_login_successful(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({
            "email": "john@example.com",
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token",
            "user_id": "12345"
        })
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        payload = {
            "email": "john@example.com",
            "password": "correctpassword"
        }
        response = self.app.post('/login', data=payload)
        
        with self.app as c:
            rv = c.get('/')
            print(session)
            assert 'access_token' in session
            assert session['email'] == 'john@example.com'
            assert session['access_token'] == 'dummy_access_token'

        self.assertEqual(response.status_code, 302)  # Expecting a redirect to ./extract

    def test_logout_clear_session(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['email'] = 'john@example.com'
                sess['access_token'] = 'dummy_access_token'
            response = c.get('/logout')
            assert 'email' not in session
            assert 'access_token' not in session
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to ./login

    @patch('requests.request')
    def test_set_new_pass_successful(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({"message": "Password updated"})
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        response = self.app.post('/new_pass/john@example.com/validcode', data={"password": "newpassword"})

        self.assertIn(b'new-pass-set', response.data)


    def test_display_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
