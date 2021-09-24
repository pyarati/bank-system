from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta
from app.models import *
from flask_script import Manager
from os import environ
from flask_cors import CORS


app1 = Flask(__name__)
app1.config['SECRET_KEY'] = '\x1f\x19\xc7\x95\xb6\xac\xd9\x1c\xbd\xd8%V\xd8\x1b@\xdf!\x13A\x9eW8\xa7\xc0'
app1.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(environ.get('DATABASE_USERNAME'), environ.get('DATABASE_PASSWORD'), environ.get('DATABASE_HOST'), environ.get('DATABASE_NAME'))
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app1.config["DEBUG"] = True
app1.config["JWT_SECRET_KEY"] = '1234567890abcdefghijklmnopqrstuvwxyz'
app1.config['PROPAGATE_EXCEPTIONS'] = True
app1.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)

#  Create a Flask-RESTPlus API
api = Api(app1)
db = SQLAlchemy(app1)
ma = Marshmallow(app1)
jwt = JWTManager(app1)
migrate = Migrate(app1, db, compare_type=True)
manager = Manager(app1)
CORS(app1)
