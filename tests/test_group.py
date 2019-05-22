import unittest

from flask import Flask

from app import db
from app.models import Group, User, JoinGroup


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        db.init_app(self.app)

        db.create_all()
        db.session.commit()

    def test_group(self):
        user_test = {
            'email' : "abcd@ff.cc",
            'password' : "abcdefg",
            'username' : "test",
        }
        user = User(**user_test)
        group = Group('TEST Group', 'This is unittest for group')
        group_member = JoinGroup(user.id, group.id)

        print(user.groups)

    def tearDown(self):
        db.session.remove()
        db.drop_all()