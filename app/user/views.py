from flask import make_response, jsonify, request, abort

from app import db, api
from app.models import User, Permission
from app.lib import jwt_required
from . import user_blueprint

@user_blueprint.route('/<userid>')
@jwt_required()
def getUser(userid):
    try:
        user = User.query.get(int(userid))

        responseObject = dict(user.as_dict())

        roles = [ role.getAsDict() for role in user.roles]
        responseObject['state'] = 'success'
        responseObject['permission'] = roles

        return make_response(jsonify(responseObject)), 200
    
    except Exception as e:
        print(e)
        responseObject = {
            'state': 'fail',
            'msg': 'User does not exists.'
        }
        return make_response(jsonify(responseObject)), 200

@user_blueprint.route('/<userid>/role', methods=['GET', 'POST'])
@jwt_required()
def Role(userid):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        if request.json:
            try:
                payload = User.validated_token(request.json['token'])
                user = User.query.filter_by(username=payload['username']).first()
                
                # TODO: Get tab owner information
                staff = user

                if staff.username == user.username:
                    role = Permission(user.id, request.json['tab_id'], role=request.json['permission'])
                    db.session.add(role)
                    db.session.commit()

                    responseObject = {
                        'state': 'success',
                        'msg': 'success create user permission'
                    }

                    return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'state': 'fail',
                    'msg': str(e)
                }
                return make_response(jsonify(responseObject)), 200


    elif request.method == 'PATCH':
        pass


    return abort(400)