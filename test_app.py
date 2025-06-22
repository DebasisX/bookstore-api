import unittest
import json
import sqlite3
from app import app, initDb, getDb
import os
import tempfile
from unittest import mock

class BookstoreTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            initDb()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    # Unit test: Mocking the database for signup
    @mock.patch('app.getDb')
    def test_unit_signup_db_error(self, mock_get_db):
        # Simulate DB integrity error
        conn = mock.MagicMock()
        curs = mock.MagicMock()
        curs.execute.side_effect = sqlite3.IntegrityError
        conn.cursor.return_value = curs
        mock_get_db.return_value = conn

        res = self.client.post(
            '/signup',
            data=json.dumps({"email": "x@x.com", "password": "pass"}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 409)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'User already exists.')

    # Integration & API tests
    def signup_and_get_cookie(self):
        # Helper to signup and login
        self.client.post(
            '/signup',
            data=json.dumps({"email": "user@test.com", "password": "testpass"}),
            content_type='application/json'
        )
        login_res = self.client.post(
            '/login',
            data=json.dumps({"email": "user@test.com", "password": "testpass"}),
            content_type='application/json'
        )
        self.assertEqual(login_res.status_code, 200)
        return login_res.headers.get('Set-Cookie')

    def test_api_signup_and_login(self):
        # Signup works
        res1 = self.client.post(
            '/signup',
            data=json.dumps({"email": "a@b.com", "password": "abc123"}),
            content_type='application/json'
        )
        self.assertEqual(res1.status_code, 201)

        # Duplicate signup
        res2 = self.client.post(
            '/signup',
            data=json.dumps({"email": "a@b.com", "password": "abc123"}),
            content_type='application/json'
        )
        self.assertEqual(res2.status_code, 409)

        # Login success
        res3 = self.client.post(
            '/login',
            data=json.dumps({"email": "a@b.com", "password": "abc123"}),
            content_type='application/json'
        )
        self.assertEqual(res3.status_code, 200)
        self.assertIn('Set-Cookie', res3.headers)

    def test_api_book_crud_operations(self):
        cookie = self.signup_and_get_cookie()

        # Create book
        book_data = {
            "title": "Sample Book",
            "author": "Author A",
            "category": "Fiction",
            "price": 12.34,
            "rating": 4.7,
            "publishedDate": "2021-05-15"
        }
        res_create = self.client.post(
            '/books',
            headers={ 'Cookie': cookie },
            data=json.dumps(book_data),
            content_type='application/json'
        )
        self.assertEqual(res_create.status_code, 201)
        created = json.loads(res_create.data)
        self.assertIn('bookId', created)
        book_id = created['bookId']

        # Read list
        res_list = self.client.get('/books', headers={ 'Cookie': cookie })
        self.assertEqual(res_list.status_code, 200)
        books = json.loads(res_list.data)['books']
        self.assertTrue(any(b['id'] == book_id for b in books))

        # Read by ID
        res_get = self.client.get(f'/books/{book_id}', headers={ 'Cookie': cookie })
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(json.loads(res_get.data)['title'], book_data['title'])

        # Update
        res_update = self.client.put(
            f'/books/{book_id}',
            headers={ 'Cookie': cookie },
            data=json.dumps({ 'title': 'Updated Title' }),
            content_type='application/json'
        )
        self.assertEqual(res_update.status_code, 200)

        # Confirm update
        res_get2 = self.client.get(f'/books/{book_id}', headers={ 'Cookie': cookie })
        self.assertEqual(json.loads(res_get2.data)['title'], 'Updated Title')

        # Delete
        res_delete = self.client.delete(f'/books/{book_id}', headers={ 'Cookie': cookie })
        self.assertEqual(res_delete.status_code, 200)

        # Confirm deletion
        res_missing = self.client.get(f'/books/{book_id}', headers={ 'Cookie': cookie })
        self.assertEqual(res_missing.status_code, 404)

    def test_book_creation_without_token(self):
        res = self.client.post(
            '/books',
            data=json.dumps({ 'title': 'NoAuth', 'author': 'NoAuth' }),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()
