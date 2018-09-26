import os
import unittest

from pymongo import MongoClient

from helpers.user_service_helper import get, post, validate_status_in_response, HttpStatusCodes
from helpers.users_helper import get_user_from_json


class TestUsersApis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = os.environ.get('API_ADDRESS', 'http://localhost:5000')
        client = MongoClient(
            os.environ.get('DB_PORT_27017_TCP_ADDR'),
            27017)
        cls.db = client.userdb

    def setUp(self):
        super().setUp()
        self.db.userdb.delete_many({})

    def test_add_user(self):
        user = get_user_from_json('uservalid1')
        response = post(self.base_url + '/adduser', data=user)
        self.assertTrue(validate_status_in_response(response, HttpStatusCodes.OK))
        self.assertIsNotNone(self.db.userdb.find_one(user))

    def test_add_user_special_characters(self):
        user_special_chars = get_user_from_json('user_special_characters')
        response = post(self.base_url + '/adduser', data=user_special_chars)
        self.assertTrue(validate_status_in_response(response, HttpStatusCodes.OK))
        self.assertIsNotNone(self.db.userdb.find_one(user_special_chars))

    def test_add_user_invalid_email(self):
        user_invalid_email = get_user_from_json('user_invalid_email')
        response = post(self.base_url + '/adduser', data=user_invalid_email)
        self.assertTrue(validate_status_in_response(response, HttpStatusCodes.BAD_REQUEST))
        self.assertIsNone(self.db.userdb.find_one(user_invalid_email))

    def test_add_user_invalid_birthdate(self):
        user_invalid_birthdate = get_user_from_json('user_invalid_birthdate')
        response = post(self.base_url + '/adduser', data=user_invalid_birthdate)
        self.assertTrue(validate_status_in_response(response, HttpStatusCodes.BAD_REQUEST))
        self.assertIsNone(self.db.userdb.find_one(user_invalid_birthdate))

    def test_get_users(self):
        user1 = get_user_from_json('uservalid1')
        user2 = get_user_from_json('uservalid2')
        self.db.userdb.insert_many([user1, user2])
        response = get(self.base_url + '/users')
        assert validate_status_in_response(response, HttpStatusCodes.OK)
        for user in response.json()['users']:
            self.assertIn(user['username'], [user1['username'], user2['username']])

    def tearDown(self):
        self.db.userdb.delete_many({})
