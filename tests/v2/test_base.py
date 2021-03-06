import os
import unittest
import json
import pytest

from app import create_app
from app.database_config import init_db


class BaseTestClass(unittest.TestCase):
    """ This is the base class has test data """

    def setUp(self):
        """ Defines the test data """

        self.app = create_app(config_name="development")
        self.client = self.app.test_client()
        self.db = init_db()

        self.data = {
            "comment": "I am doing it",
            "createdBy": 1,
            "createdOn": "2018-12-12 15:45:07",
            "images": "images.jpg",
            "location": "naironi",
            "status": "Draft",
            "incidentType": "Redflag",
            "videos": "videos.mp4"
        }

        self.no_input = {
        }

        self.auth_signup = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "R",
            "username": "testuser",
            "email": "test@test.com",
            "phonenumber": "0724716026",
            "password": "Eatlivecode2@",
            "isAdmin": True
        }

        self.no_comment = {
            "comment": "",
            "createdBy": 1,
            "createdOn": "2017-12-12 15:45:07",
            "images": "images.jpg",
            "location": "naironi",
            "status": "Draft",
            "incidentType": "Redflag",
            "videos": "videos.mp4"    
        }

        self.token_login = {
            "username": "testuser",
            "password": "Eatlivecode2@"
        }
        self.auth = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "Right",
            "username": "testusr",
            "email": "test@tst.com",
            "phonenumber": "0717245111",
            "password": "Eatlivecode3@",
            "isAdmin": False
        }
        self.cell = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "Right",
            "username": "usertesting",
            "email": "usertesting@tst.com",
            "phonenumber": "0717245111",
            "password": "Eatlivecode3@",
            "isAdmin": False
        }
        self.email = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "Right",
            "username": "emailtesting",
            "email": "test@tst.com",
            "phonenumber": "0717245191",
            "password": "Eatlivecode3@",
            "isAdmin": False
        }
        self.username = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "Right",
            "username": "testusr",
            "email": "usernametesting@tst.com",
            "phonenumber": "0717245911",
            "password": "Eatlivecode3@",
            "isAdmin": False
        }
        self.login = {
            "username": "testusr",
            "password": "Eatlivecode3@"
        }
        self.invalid = {
            "username": "Andela1",
            "password": "Eatlivecod4@"
        }
        self.unregistered = {
            'username': 'ramsaybolton',
            'password': 'darkthoughts@1'
        }
        self.duplicate = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "Right",
            "username": "testusr",
            "email": "test@tst.com",
            "phonenumber": "0717245111",
            "password": "Eatlivecode3@",
            "isAdmin": False
        }
        self.missing_fields = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "Right",
            "email": "test@tst.com",
            "phonenumber": "0717245111",
            "password": "Eatlivecode3@",
            "isAdmin": False
        }

        res = self.client.post(
            '/api/v2/signup',
            data=json.dumps(self.auth_signup),
            headers={"content-type": "application/json"}
        )

        login_res = self.client.post(
            '/api/v2/login',
            data=json.dumps(self.token_login),
            headers={"content-type": "application/json"}
        )
        response = json.loads(login_res.data.decode())
        self.auth_token = response["access_token"]

    def tearDown(self):

        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""DROP TABLE IF EXISTS users CASCADE """)
        curr.execute("""DROP TABLE IF EXISTS incidents CASCADE """)
        dbconn.commit()


if __name__ == "__main__":
    unittest.main()
