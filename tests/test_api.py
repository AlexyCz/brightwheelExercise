import sys
import unittest
import json

sys.path.append('../')
import api

POST_URL = 'http://localhost:5000/email'

class TestAPI(unittest.TestCase):
    """Unit tests for email service POST endpoint"""
    def setUp(self):
        self.app = api.app.test_client()
        self.app.testing = True

    def post_test(self):
        """" Test 1: required field missing """
        body = {
            "to_name": "Mr. Fake",
            "from": "noreply@mybrightwheel.com", 
            "from_name": "Brightwheel",
            "subject": "A Message from Brighwheet", 
            "body": "<h1>Your Bill</h><p>$10</p>"
            }
        response = self.app.post(POST_URL, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)

        """" Test 2: required field incorrect type """
        body = {
            "to": "fake@fake.com"
            "to_name": "Mr. Fake",
            "from": 123, 
            "from_name": "Brightwheel",
            "subject": "A Message from Brighwheet", 
            "body": "<h1>Your Bill</h><p>$10</p>"
            }
        response = self.app.post(POST_URL, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)


        """" Test 3: all validation checks passed """
        body = {
            "to": "fake@fake.com"
            "to_name": "Mr. Fake",
            "from": "noreply@mybrightwheel.com", 
            "from_name": "Brightwheel",
            "subject": "A Message from Brighwheet", 
            "body": "<h1>Your Bill</h><p>$10</p>"
            }
        response = self.app.post(POST_URL, data=json.dumps(body))
        self.assertEqual(response.status_code, 200)
        