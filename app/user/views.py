from flask import make_response, jsonify, request, abort

from app.models import User, Permission
from . import user_blueprint

@user_blueprint.route('/<userid>')
def getUser(userid):
    try:
        user = User.query.get(int(userid))
        responseObject = dict(user.as_dict())
        responseObject['state'] = 'success'
        return make_response(jsonify(responseObject)), 200
    
    except Exception as e:
        responseObject = {
            'state': 'fail',
            'msg': 'User does not exists.'
        }
        return make_response(jsonify(responseObject)), 200

@user_blueprint.route('/<userid>/role', methods=['GET', 'POST'])
def Role(userid):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        if request.json:
            try:
                username = User.validated_token(request.json['token'])
                user = User.query.filter(username=username).first()
                

                # TODO: Get tab owner information
                staff = user

                if staff.username == user.username:
                    role = Permission(user.id, request.json['tab_id'], permission=request.json['permission'])
                    db.session.add(role)
                    db.commit()

                    responseObject = {
                        'state': 'success',
                        'msg': 'success create user permission'
                    }

                    return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'state': 'success',
                    'msg': str(e)
                }
                return make_response(jsonify(responseObject)), 200


    elif request.method == 'PATCH':
        pass


    return abort(400)