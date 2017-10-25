import unittest
from project import app, db
from project.users.models import User
from flask_testing import TestCase
from flask import json
from project.helpers import authenticate, _user_login

class TestApp(TestCase):
    user_login = _user_login

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['ENV'] = 'testing'
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        user1 = User('bigrobsf', 'apassword', 'Rob', 'Conner', 'rob@conner.com')
        db.session.add(user1)
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_create_user_success(self):
        response = self.client.post('/api/users',
            headers={
                'Content-Type':'application/json'
            },
            data=json.dumps({
                'user_name': 'newuser',
                'password': 'something',
                'first_name': 'New',
                'last_name': 'User',
                'email': 'new_user@gmail.com'})
        )
        expected_json = {
            'id': 2,
            'user_name': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new_user@gmail.com'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_json)
        self.assertEqual(User.query.count(), 2) 

    def test_create_user_dup_username(self):
        response = self.client.post('/api/users',
            headers={
                'Content-Type':'application/json'
            },
            data=json.dumps({
                'user_name': 'bigrobsf',
                'password': 'something',
                'first_name': 'Not',
                'last_name': 'Rob',
                'email': 'not_rob@gmail.com'})
        )
        expected_json = {
            'message': 'User name already exists'
        }
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, expected_json)
        self.assertEqual(User.query.count(), 1)

    def test_create_user_dup_email(self):
        response = self.client.post('/api/users',
            headers={
                'Content-Type':'application/json'
            },
            data=json.dumps({
                'user_name': 'anewuser',
                'password': 'something',
                'first_name': 'Jim',
                'last_name': 'Bob',
                'email': 'rob@conner.com'})
        )
        expected_json = {
            'message': 'Email already registered'
        }
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, expected_json)
        self.assertEqual(User.query.count(), 1) 

    def test_user_login_success(self):
        response = self.client.post('/api/users/auth',
            content_type='application/json',
            data=json.dumps({'username': 'bigrobsf',
                'password': 'apassword'})
        )
        token = authenticate('bigrobsf', 'apassword')
        expected_json = {'token': token}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_json)

    def test_user_login_fail(self):
        response = self.client.post('/api/users/auth',
            content_type='application/json',
            data=json.dumps({
                'user_name': 'bigrobsf',
                'password': 'badpassword'})
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'message': 'Invalid Credentials'})

    def test_get_user_success(self):
        response = self.client.get('/api/users/1',
            headers={
                'Content-Type': 'application/json'
            }
        )
        expected_json = {
            'id': 1,
            'user_name': 'bigrobsf',
            'first_name': 'Rob',
            'last_name': 'Conner',
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_json)
        self.assertEqual(User.query.count(), 1)

    def test_edit_user_success(self):
        user_auth = self.user_login(
            username='bigrobsf',
            password='apassword'
        )
        response = self.client.patch('/api/users/1',
            headers={
                'authorization': 'bearer ' + user_auth['token'],
                'Content-Type': 'application/json'
            },
            data=json.dumps({'email': 'robert@conner.com'})
        )
        expected_json = {
            'id': 1,
            'email': 'robert@conner.com'
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_json)
        self.assertEqual(User.query.count(), 1)

    def test_edit_user_unauthorized(self):
        response = self.client.patch('/api/users/1',
            headers={
                'Content-Type':'application/json'
            },
            data=json.dumps({'email': 'new_email@gmail.com'})
        )
        expected_json = {
            'message': 'Please log in again'
        }
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, expected_json)

if __name__ == '__main__':
    unittest.main()