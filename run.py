from app import app
from app.routes import *
from app import db


if __name__ == '__main__':
    #  Start a development server
    app.run(host='0.0.0.0')
