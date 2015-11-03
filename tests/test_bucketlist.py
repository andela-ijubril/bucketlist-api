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

        db.create_all()

        user = User(
            username="jubril",
            email="jubril@somedomain.com",
            password_hash="chiditheboss"
        )
        db.session.add(user)
        db.session.commit()

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

    def test_create_bucketlist(self):

        response = self.client.post(
            url_for('api.create_bucketlist'),
            headers=self.get_api_headers('jubril', 'chiditheboss'),
            data=json.dumps({
                'name': 'My first Bucketlist',
            })
        )

        self.assertTrue(response.status_code == 200)