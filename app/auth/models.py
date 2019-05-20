import re
import datetime

import jwt
from sqlalchemy.orm import validates


from app import db, bcrypt


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(5), default='user')

    def __init__(self, email, username):
        self.email = email
        self.username = username

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
                'idat': datetime.datetime.utcnow(),
                'sub':self.username,
                'role': self.role,
            }
            return jwt.encode(payload, app.config.get('SECRET_KEY'), algorithm='HS256')
        except Exception as e:
            return e

    def __repr__(self):
        return self.username