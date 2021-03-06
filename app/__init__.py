from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_marshmallow import Marshmallow
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x1f\x19\xc7\x95\xb6\xac\xd9\x1c\xbd\xd8%V\xd8\x1b@\xdf!\x13A\x9eW8\xa7\xc0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mySQL@123@localhost/bank_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True


#  Create a Flask-RESTPlus API
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
