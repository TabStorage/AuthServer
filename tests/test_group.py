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

        db.session.add(user)
        db.session.add(group)
        db.session.commit()

        group_member = JoinGroup(user.id, group.id)

        db.session.add(group_member)
        db.session.commit()

        self.assertEqual(user.groups[0], group_member)

    def tearDown(self):
        db.session.remove()
        db.drop_all()