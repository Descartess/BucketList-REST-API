""" unit tests for authentication api """
import json
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
            self.assertIn("Paul", data['message'])

    def test_register_user_invalid_json(self):
        """ Ensure that error is returned on invalid json """
        with self.client:
            response = self.client.post(
                'auth/register', data=json.dumps(dict()), content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual('Invalid payload', data['message'])
            self.assertEqual('Fail', data['status'])

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

    def test_add_duplicate_user(self):
        """ Ensure that an error is returned on a duplicate user registration """
        with self.client:
            self.client.post(
                'auth/register',
                data=json.dumps(dict(username="Paul", password="test")),
                content_type="application/json"
            )
            response = self.client.post(
                'auth/register',
                data=json.dumps(dict(username="Paul", password="test")),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry username already is taken", data['message'])
            self.assertIn("Fail", data['status'])
            