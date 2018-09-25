import os
import unittest

from pymongo import MongoClient

from user_service_helper import get, post, validate_status_in_response, HttpStatusCodes


class TestUsersApis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = os.environ.get('API_ADDRESS')
        client = MongoClient(
            os.environ.get('DB_PORT_27017_TCP_ADDR'),
            27017)
        cls.db = client.userdb
        cls.user_data1 = {
            "username": "usertest",
            "emailaddress": "usertest@dwdwd.com",
            "birthdate": "2014-12-31",
            "address": "street 123123"
        }
        cls.user_data2 = {
            "username": "usertest2",
            "emailaddress": "usertest2@dwdwd.com",
            "birthdate": "2005-03-05",
            "address": "myaddress 0123"
        }
        cls.user_invalid_email = {
            "username": "theuser",
            "emailaddress": "theuserinvalidemail",
            "birthdate": "2015-03-05",
            "address": "theaddress 0123"
        }
        cls.user_invalid_birthdate = {
            "username": "anotheruser",
            "emailaddress": "anotheruser@hotmail.com",
            "birthdate": "9000-03-05",
            "address": "myaddress 0123"
        }

    def setUp(self):
        super().setUp()
        self.db.userdb.delete_many({})

    def test_add_user(self):
        response = post(self.base_url + '/adduser', data=self.user_data1)
        self.assertTrue(validate_status_in_response(response, HttpStatusCodes.OK))
        self.assertIsNotNone(self.db.userdb.find_one(self.user_data1))

    def test_add_user_invalid_email(self):
        response = post(self.base_url + '/adduser', data=self.user_invalid_email)
        self.assertTrue(validate_status_in_response(response, HttpStatusCodes.BAD_REQUEST))
        self.assertIsNone(self.db.userdb.find_one(self.user_invalid_email))

    def test_add_user_invalid_birthdate(self):
        response = post(self.base_url + '/adduser', data=self.user_invalid_birthdate)
        self.assertTrue(validate_status_in_response(response, HttpStatusCodes.BAD_REQUEST))
        self.assertIsNone(self.db.userdb.find_one(self.user_invalid_birthdate))

    def test_get_users(self):
        self.db.userdb.insert_many([self.user_data1, self.user_data2])
        response = get(self.base_url + '/users')
        assert validate_status_in_response(response, HttpStatusCodes.OK)
        for user in response.json()['users']:
            self.assertIn(user['username'], [self.user_data1['username'], self.user_data2['username']])

    def tearDown(self):
        self.db.userdb.delete_many({})
