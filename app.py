from flask import Flask, Response, jsonify
from Auth import auth

class JsonResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JsonResponse, cls).force_type(rv, environ)

app = Flask(__name__)
app.config.from_object('config')
app.response_class = JsonResponse

@app.route('/')
def hello_world():
    return {'hello_world':'hi'}

    