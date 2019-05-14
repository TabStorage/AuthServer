from flask import Blueprint, make_response, jsonify, request


from app import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    test = {'1': 1}


    return make_response(jsonify(request)), 200


@auth.route('/join', methods=['POST'])
def join():
    test = {'1': 1}


    return make_response(jsonify(request)), 200

