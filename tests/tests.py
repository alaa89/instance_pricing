import unittest
import json
from instance_pricing import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_404(self):
        response = self.client.get(
            '/wrong/url')
        self.assertTrue(response.status_code == 404)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'Not found')

    def test_valid_search(self):
        response = self.client.get(
            '/v1/pricing?instance_type=m1.large&region=us-east-1')
        self.assertTrue(response.status_code == 200)

    def test_invalid_search(self):
        response = self.client.get(
            '/v1/pricing?instance_type=r3.xlarge&region=eu-west-1')
        self.assertTrue(response.status_code == 404)

    def test_post_request(self):
        # write an empty post
        response = self.client.post(
            '/v1/pricing',
            data=json.dumps({}))
        self.assertTrue(response.status_code == 422)

        # write a post
        response = self.client.post(
            '/v1/pricing',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'instance_type': 'm1.large', 'region': 'us-east-1'}))
        self.assertTrue(response.status_code == 200)

    def test_missing_headers(self):
        response = self.client.post(
            '/v1/pricing',
            data=json.dumps({'instance_type': 'm1.large', 'region': 'us-east-1'}))
        self.assertTrue(response.status_code == 422)

    def test_method_not_allowed(self):
        response = self.client.put(
            '/v1/pricing',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'instance_type': 'm1.large', 'region': 'us-east-1'}))
        self.assertTrue(response.status_code == 405)


if __name__ == '__main__':
    unittest.main()
