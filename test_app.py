import unittest
import json
from app import app, initDb
import os
import tempfile

class BookTest(unittest.TestCase):
    def setUp(self):
        self.dbFd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            initDb()
    
    def tearDown(self):
        os.close(self.dbFd)
        os.unlink(app.config['DATABASE'])
    
    def testSignupLogin(self):
        res1 = self.client.post(
            '/signup',
            data=json.dumps({"email": "test@example.com", "password": "testpass"}),
            content_type="application/json"
        )
        self.assertEqual(res1.status_code, 201)
        data1 = json.loads(res1.data)
        self.assertIn("message", data1)
        self.assertEqual(data1["message"], "User created successfully.")

        res2 = self.client.post(
            '/signup',
            data=json.dumps({"email": "test@example.com", "password": "testpass"}),
            content_type="application/json"
        )
        self.assertEqual(res2.status_code, 409)

        res3 = self.client.post(
            '/login',
            data=json.dumps({"email": "test@example.com", "password": "testpass"}),
            content_type="application/json"
        )
        self.assertEqual(res3.status_code, 200)
        data3 = json.loads(res3.data)
        self.assertIn("token", data3)
    
    def testBookNoToken(self):
        res = self.client.post(
            '/books',
            data=json.dumps({
                "title": "Sample Book", 
                "author": "Author Name", 
                "category": "Fiction",
                "price": 9.99, 
                "rating": 4.5, 
                "publishedDate": "2020-01-01"
            }),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()
