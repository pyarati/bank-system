from app import app1
from app.routes import *
from app import db
from app import manager


if __name__ == '__main__':
    #  Start a development server
    app1.run(host='0.0.0.0')

