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

        self.assertIn(b'Email already taken', response.data)

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
        self.assertEqual(response.status_code, 200)

    @patch('requests.request')
    def test_reset_pass_post_email_error(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({"error_code": "u001"})
        mock_response.status_code = 400
        mock_request.return_value = mock_response

        response = self.app.post('/reset_pass', data={"email": "noemail@example.com"})

        self.assertIn(b'Password not set please try again', response.data)

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

        self.assertIn(b'We have sent you an email', response.data)

    @patch('requests.request')
    def test_reset_pass_post_email_send_fail(self, mock_request):
        # Mocking a non u001 error from the EMAIL_API_URL
        mock_response = Mock()
        mock_response.text = json.dumps({"error_code": "u002", "message": "Unknown error"})
        mock_response.status_code = 400
        mock_request.return_value = mock_response

        response = self.app.post('/reset_pass', data={"email": "existingemail@example.com"})

        self.assertNotIn(b'Password not set please try again', response.data)

    @patch('requests.request')
    def test_set_new_pass_invalid_code(self, mock_request):
        mock_response = Mock()
        mock_response.text = json.dumps({"message": "Invalid code"})
        mock_response.status_code = 400
        mock_request.return_value = mock_response

        response = self.app.post('/new_pass/existingemail@example.com/invalidcode', data={"password": "newpassword"})

        self.assertIn(b'Invalid code', response.data)

    @patch('requests.request')
    def test_successful_login(self, mock_request):

        # Mock successful response
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
        with self.app as c:
            response = c.post('/login', data=payload)

            # Debugging prints
            print("Mock Response:", mock_response.text)
            print("Actual Response:", response.data)

            print(session.get('email'))
            print('****')
            self.assertEqual(session['email'], "john@example.com")
            self.assertEqual(session['access_token'], "dummy_access_token")

    @patch('requests.request')
    def test_invalid_credentials(self, mock_request):

        # Mock failure response
        mock_response = Mock()
        mock_response.text = json.dumps({"message": "Invalid credentials"})
        mock_response.status_code = 401  # or whatever status code indicates invalid creds
        mock_request.return_value = mock_response

        payload = {
            "email": "john@example.com",
            "password": "wrongpassword"
        }
        response = self.app.post('/login', data=payload)
        self.assertIn(b'Invalid email or password', response.data)

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

        self.assertIn(b'Your password has been set', response.data)

    def test_display_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
