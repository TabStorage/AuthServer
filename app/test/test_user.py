import unittest

from flask import Flask

from app import db
from app.auth.models import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        db.init_app(self.app)

        db.create_all()
        db.session.commit()

    def test_common_user(self):
        user_test = {
            'email' : "abcd@ff.cc",
            'password' : "abcdefg",
            'username' : "test",
        }
        user = User(**user_test)
        self.assertTrue(user.validated_password(user_test['password']))
        self.assertFalse(user.validated_password('1234'))

        db.session.add(user)
        db.session.commit()

        test = User.query.filter_by(username='test').first()
        self.assertTrue(user == test)

        token = user.generate_token()

        self.assertEqual(user_test['username'], User.validated_token(token))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

