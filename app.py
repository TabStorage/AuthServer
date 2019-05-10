from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import auth


# Define response class
class JsonResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JsonResponse, cls).force_type(rv, environ)

# Set Flask setting
app = Flask(__name__)
app.config.from_object('config')
app.response_class = JsonResponse
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return {'hello_world':'hi'}

