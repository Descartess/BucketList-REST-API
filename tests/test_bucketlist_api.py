""" unit tests for the bucketlist api """
import json
from .test_base import BaseTestCase

class TestBucketListCase(BaseTestCase):
    """ unit tests for the bucketlist api """
    def test_create_bucket_lists(self):
        """ Ensure that bucketlists can be created """
        with self.client:
            response = self.client.post(
                'bucketlists',
                data=json.dumps(dict(name="Career", completed_by=30)),
                content_type="application/json",
                headers=dict(Authorization='Bearer '+ self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['status'], "Success")

    def test_get_bucket_lists(self):
        """ Ensure that bucketlists can be retrieved """
        with self.client:
            response = self.client.get(
                'bucketlists',
                content_type="application/json",
                headers=dict(Authorization='Bearer '+ self.token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(data, {'bucketlists': []})

    def test_no_auth_token(self):
        """ Ensure that error is returned with no headers """
        with self.client:
            response = self.client.post(
                'bucketlists',
                data=json.dumps(dict(name="Career", completed_by=30)),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'],'Provide valid auth Token')

