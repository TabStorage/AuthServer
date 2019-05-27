from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate, upgrade
from flask_restplus import Api

from config import config


# define extension
db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api()

def create_app(mode):
    # Set Flask setting
    app = Flask(__name__)
    app.config.from_object(config[mode])

    # Set extension
    db.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)

    # Register blueprint
    from app.auth import auth_blueprint
    from app.user import user_blueprint
    from app.group import group_blueprint
    from app.swagger import swagger

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(group_blueprint, url_prefix='/group')

    return app



