from functools import wraps

from flask import request, make_response, jsonify

from app.models import User
def jwt_required(required_role='user'):
    def inner_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: implement
            try:
                token = request.cookies.get('TABFARM_TOKEN')
                user = User.validated_token(token)

                if user['role'] != required_role:
                    return make_response(jsonify({
                    "msg": "you can't access",
                    "status": "fail"
                    })), 201

                result = func(*args, **kwargs)

            except Exception as e:
                print("jwt_reuqired logic")
                return make_response(jsonify({
                    "msg": str(e),
                    "status": "fail"
                })), 201

            return result
        return wrapper
    return inner_func