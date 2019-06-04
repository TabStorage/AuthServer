from functools import wraps

from flask import request, make_response, jsonify

from app.models import User
def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: implement
        try:
            token = request.cookies.get('TABFARM_TOKEN')
            User.validated_token(token)
            print("jwt_reuqired logic")
            result = func(*args, **kwargs)

        except Exception as e:
            return make_response(jsonify({
                "msg": str(e),
                "status": "fail"
            })), 201

        return result
    return wrapper