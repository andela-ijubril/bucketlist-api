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
            password_hash="chiditheboss"
        )
        db.session.add(user)
        db.session.commit()
        g.user = user

        self.client = self.app.test_client()





        test_user = User(username="padi", email="padi@gmail.com", password_hash="padimi")



        test_user.save()
        bucketlist = Bucketlist(name="padi Bucketlist", created_by = g.user.id)
        bucketlist.save()
        item = Item(
            name="Item of the padi bucketlist", bucketlist_id=bucketlist.id
        )

        item.save()
        self.client = self.app.test_client()



        # log the user in and get authentication token:
        # response = self.client.post(
        #     url_for('login'),
        #     headers=self.get_api_headers(),
        #     data=json.dumps({
        #         'username': 'jubril',
        #         'password': 'anything',
        #     })
        # )
        # self.access_token = json.loads(response.data).get('access_token')

        # fix the db with sample bucketlists for the user:
        # bucketlist_1 = Bucketlist(name="The test Wishlist", created_by=self.user)
        # db.session.add(bucketlist_1)
        # db.session.commit()
        #
        # # fix the db with sample bucketlists items for the bucketlist_3:
        # item_1 = Item(name="Bungee off the Brooklyn Bridge", done=False, bucketlist=bucketlist_1)
        # db.session.add(item_1)
        # item_2 = Item(name="Kayak across the Atlantic", done=False, bucketlist=bucketlist_1)
        # db.session.add(item_2)
        # item_3 = Item(name="Scuba dive in the Mariannah Trench", done=False, bucketlist=bucketlist_1)
        # db.session.add(item_3)
        # db.session.commit()

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
        token = self.get_token()
        response = self.client.put(
            url_for('api_1.bucketitem',
                    bucketlist_id=1, bucketitem_id=1),
            headers=self.get_api_headers(token, 'password'),
            data=json.dumps({'name': 'I just changed this bucketlist'}))
        self.assertTrue(response.status_code == 200)


        response = self.client.put(
            url_for('api.bucket_item', bucketlist_id=1, item_id=1),
            headers=self.get_api_headers('jubril', 'chiditheboss'),
            data=json.dumps({
                'name': 'My first Bucketlist Item',
                'done': True
            })
        )

        response_data = json.loads(response.data)
        bucketlist_item = response_data.get('bucketlist_item')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(bucketlist_item.get('done'), False)

    def test_delete_bucket_item(self):
        response = self.client.delete(
            url_for('api.bucket_item', bucketlist_id=1, item_id=1),
            headers=self.get_api_headers('jubril', 'chiditheboss'),
        )

        self.assertTrue(response.status_code == 200)
