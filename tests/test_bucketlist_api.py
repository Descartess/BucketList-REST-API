""" unit tests for the bucketlist api """
import json
from app import create_app, db
from .test_base import BaseTestCase


class TestBucketListCase(BaseTestCase):
    """ unit tests for the bucketlist api """

    def setUp(self):
        """initial setup before a test is run """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(self)
        db.create_all()
        # log in a user
        resp = self.client.post(
            'auth/register',
            data=json.dumps(
                dict(username='testuser', password='testpassword')),
            content_type='application/json'
        )
        self.token = json.loads(resp.data.decode())['token']
        # create bucket list
        self.response = self.client.post(
            'bucketlists',
            data=json.dumps(dict(name="Career", completed_by=30)),
            content_type="application/json",
            headers=dict(Authorization='Bearer ' + self.token)
        )

    def test_create_bucket_lists(self):
        """ Ensure that bucketlists can be created and retrieved """
        with self.client:
            data = json.loads(self.response.data.decode())
            self.assertEqual(self.response.status_code, 201)
            self.assertEqual(data['status'], "Success")
            get_response = self.client.get(
                'bucketlists',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(get_response.data.decode())
            self.assertEqual(get_response.status_code, 200)
            self.assertDictEqual(data, {'bucketlists': [{
                "id": 1,
                "name": "Career",
                "completed_by": 30
            }]})

    def test_no_auth_token(self):
        """ Ensure that error is returned with no headers """
        with self.client:
            response = self.client.post(
                'bucketlists',
                data=json.dumps(dict(name="Career", completed_by=30)),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide valid auth Token')

    def test_get_bucketlists_with_id(self):
        """ Ensure that buckelists with data can be retrieved using IDs """
        with self.client:
            response = self.client.get(
                'bucketlists/1',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'bucketlist': {
                "id": 1,
                "name": "Career",
                "completed_by": 30
            }})

    def test_update_bucketlists_with_id(self):
        """ Ensure that buckelists with data can be updated using IDs """
        with self.client:
            response = self.client.put(
                'bucketlists/1',
                data=json.dumps(dict(name="Adventure", completed_by=25)),
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'bucketlist': {
                "id": 1,
                "name": "Adventure",
                "completed_by": 25
            }})

    def test_delete_bucketlists_with_id(self):
        """ Ensure that buckelists with data can be deleted using IDs """
        with self.client:
            response = self.client.delete(
                'bucketlists/1',
                content_type="application/json",
                headers=dict(Authorization='Bearer ' + self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'bucketlist': {}})
