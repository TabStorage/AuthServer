from flask import Blueprint, make_response, jsonify, request

from app import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)

    try:
        user = User.query.filter_by(email=request.json['email']).first()
        if user.validated_password(request.json['password']):
            token = user.generate_token()
            responseObject = {
                'status': 'success',
                'token': token.decode(),
            }
            return make_response(jsonify(responseObject)), 200

        else:
            responseObject = {
                'status': 'fail',
                'msg': 'User does not exist.',
            }
            return make_response(jsonify(responseObject)), 200

    except Exception as e:
        responseObject = {
            'status': 'fail',
            'msg': 'Some error occured.'
        }

@auth.route('/join', methods=['POST'])
def join():
    if not request.json:
        abort(400)

    try:
        user = User(username=request.json['username'], email=request.json['email'])
        user.set_password(request.json['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(msg="User successfully created", user_id=user.id), 200
    
    except AssertionError as ex:
        return jsonify(msg=f"Error: {ex}."), 400

