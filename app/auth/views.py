from flask import Blueprint, make_response, jsonify, request

from app import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)

    return make_response(jsonify(request)), 200


@auth.route('/join', methods=['POST'])
def join():
    if not request.json:
        abort(400)
    user = User(username=request.json['username'], email=request.json['email'])
    user.set_password(request.json['password'])

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(msg="User successfully created", user_id=user.id), 200
    
    except AssertionError as ex:
        return jsonify(msg=f"Error: {ex}."), 400

