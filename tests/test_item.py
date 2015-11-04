from base64 import b64encode
import json
import unittest

from api.models import Bucketlist, User, Item
from flask import url_for, g
from api import create_app, db


class TestAPI(unittest.TestCase):

    def setUp(self):

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()

        user = User(
            username="jubril",
            email="jubril@isere.com",
        )
        user.hash_password("chiditheboss")
        db.session.add(user)
        db.session.commit()
        g.user = user

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization':
                'Basic ' + b64encode(
                    (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_user_token(self):
        # calls the login function and returns the token generated
        response = self.client.post(
            url_for('api.login'),
            headers=self.get_api_headers('jubril', 'chiditheboss'),
            data=json.dumps({'username': 'jubril', 'password': 'chiditheboss'}))
        token = json.loads(response.data)['token']
        return token

    def test_create_bucketlist_item(self):

        response = self.client.post(
            url_for('api.create_item', bucketlist_id=1),
            headers=self.get_api_headers('jubril', 'chiditheboss'),
            data=json.dumps({
                'name': 'My first Bucketlist Item',
                'done': False
            })
        )

        self.assertTrue(response.status_code == 200)

    def test_update_bucket_item(self):
        token = self.get_user_token()
        response = self.client.put(
            url_for('api.bucket_item',
                    bucketlist_id=1, item_id=1),
            headers=self.get_api_headers(token, 'chiditheboss'),
            data=json.dumps({'name': 'I just changed this bucketlist', 'done': True}))
        self.assertTrue(response.status_code == 200)

    def test_delete_bucket_item(self):
        token = self.get_user_token()
        response = self.client.delete(
            url_for('api.bucket_item', bucketlist_id=1, item_id=1),
            headers=self.get_api_headers(token, 'chiditheboss'),
        )

        self.assertTrue(response.status_code == 200)

