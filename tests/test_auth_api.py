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
                    username='Paul'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("Paul", data['message'])
