import re
import datetime
import datetime

import jwt
from sqlalchemy.orm import validates, backref
from flask import current_app

from app import db, bcrypt


class User(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(5), default='user')
    joined_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, email, username, role='user', password=None):
        self.email = email
        self.username = username
        self.role = role

        if password is not None:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def validated_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @validates('email')
    def validated_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        
        if User.query.filter(User.email == email).first():
            raise AssertionError('Email is already in used')

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not an email address')

        return email

    @validates('username')
    def validated_name(self, key, name):
        if not name:
            raise AssertionError('No name provided')
        
        if User.query.filter(User.username == name).first():
            raise AssertionError('Username is already in used')

        return name

    def generate_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3),
                'iat': datetime.datetime.utcnow(),
                'sub': self.username,
                'role': self.role,
                'user_id': self.id

            }
            return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def validated_token(token):
        try: 
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))

            return payload
        
        except jwt.exceptions.ExpiredSignatureError:
            return 'token was expired'
        
        except jwt.exceptions.InvalidTokenError:
            return 'token was wrong'

        except jwt.DecodeError:
            return 'token decode error'

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role
        }

    def __repr__(self):
        return self.username

class Group(db.Model):
    __table_name__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200), nullable=True)
    type = db.Column(db.Integer, nullable=False)

    # members = db.relationship("JoinGroup")
    
    def __init__(self, group_name, description, type=0):
        self.group_name = group_name
        self.description = description
        self.type = 0

class JoinGroup(db.Model):
    __table_name__ = 'group_members'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id), nullable=False)
    joined_date = db.Column(db.DateTime, default=datetime.datetime.now)

    user = db.relationship("User", backref=backref('groups', cascade="all, delete-orphan"))
    group = db.relationship("Group", backref=backref('members', cascade="all, delete-orphan"))

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id

class Permission(db.Model):
    __table_name__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    role = db.Column(db.Integer, default=0)
    root_tab_id = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref=backref('roles', cascade="all, delete-orphan"))

    def __init__(self, userid, root_tab_id, role=0):
        self.user_id = userid
        self.role = role
        self.root_tab_id = root_tab_id

    def getAsDict(self):
        return {self.root_tab_id : self.role}
