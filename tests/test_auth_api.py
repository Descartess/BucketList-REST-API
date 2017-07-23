""" unit tests for authentication api """
import json
from app.utils import add_user
from .test_base import BaseTestCase


class TestAuthCase(BaseTestCase):
    """ unit tests for authentication api """

    def test_register_user(self):
        """ Ensure that users get registered """
        with self.client:
            response = self.client.post(
                'auth/register',
                data=json.dumps(dict(
                    username='Paul',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'Paul')
            self.assertTrue(data['token'])

    def test_register_user_invalid_json(self):
        """ Ensure that error is returned on invalid json """
        with self.client:
            response = self.client.post(
                'auth/register', data=json.dumps(dict()), content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual('Invalid payload', data['message'])
            self.assertEqual('Fail', data['status'])
            self.assertIsNone(data['token'])

    def test_register_user_invalid_keys(self):
        """ Ensure that error is returned on missing/invalid keys """
        with self.client:
            response = self.client.post(
                'auth/register', data=json.dumps(dict(username="Paul")),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual('Invalid payload', data['message'])
            self.assertEqual('Fail', data['status'])
            self.assertIsNone(data['token'])

    def test_add_duplicate_user(self):
        """ Ensure that an error is returned on a duplicate user registration """
        with self.client:
            add_user("Paul", "password")
            response = self.client.post(
                'auth/register',
                data=json.dumps(dict(username="Paul", password="test")),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry username already is taken", data['message'])
            self.assertIn("Fail", data['status'])
            self.assertIsNone(data['token'])

    def test_user_correct_login(self):
        """ Ensure that user logs in with correct credentials"""
        with self.client:
            add_user(username="Paul", password="password")
            response = self.client.post(
                'auth/login',
                data=json.dumps(dict(username="Paul", password="password")),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Success", data['status'])

    def test_user_incorrect_password(self):
        """ Ensure that user doesnt logs in with incorrect credentials"""
        with self.client:
            add_user(username="Paul", password="password")
            response = self.client.post(
                'auth/login',
                data=json.dumps(dict(username="Paul", password="qwerty")),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Fail", data['status'])

    def test_user_incorrect_username(self):
        """ Ensure that user doesnt logs in with incorrect credentials"""
        with self.client:
            response = self.client.post(
                'auth/login',
                data=json.dumps(dict(username="Laura", password="qwerty")),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Fail", data['status'])
