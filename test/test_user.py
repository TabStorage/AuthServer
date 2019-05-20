import unittest

from flask import Flask

from tabfarm.app import db
from models import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def test_common_user(self):
        user_test = {
            'email' : "abcd@ff.cc",
            'password' : "abcdefg",
            'username' : "test"
        }
        user = User(**user_test)
        self.assertTrue(user.validated_password(user_test['password']))
        self.assertFalse(user.validated_password('1234'))

        db.session.add(user)
        db.session.commit()

        test = User.query.filter_by(username='test').first()
        self.assertTrue(user == test)

