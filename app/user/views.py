from flask import make_response, jsonify

from app.models import User
from . import user_blueprint


@user_blueprint.route('/<userid>')
def getUser(userid):
    try:
        user = User.query.filter(id=userid)
        responseObject = dict(user.as_dict())
        responseObject['state'] = 'success'
        return make_response(jsonify(responseObject)), 200
    
    except Exception as e:
        responseObject = {
            'state': 'fail',
            'msg': 'User does not exists.'
        }
        return make_response(jsonify(responseObject)), 200