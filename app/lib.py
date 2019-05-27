from functools import wraps

from flask import request

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: implement
        print("jwt_reuqired loginc")
        result = func(*args, **kwargs)
        return result
    return wrapper