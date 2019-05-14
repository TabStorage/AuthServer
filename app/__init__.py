from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import DevelopmentConfig


# Set Flask setting
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


# Set extension
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


# Register blueprint
from app.auth.views import auth as auth_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')



