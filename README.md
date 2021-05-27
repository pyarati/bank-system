# Bank Transaction System

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Bank Transaction System can be used by bank customers to perform day to day operations like create/update user, create/update account, deposit amount to the account, withdraw amount from the account, etc.

## Technologies
Project is created with:
* Python: 3.8.5

## Setup
To run this project, 
Use the package manager [pip](https://pip.pypa.io/en/stable/)

### Flask
**Flask** is a popular Python web framework, meaning it is a third-party Python library used for developing web applications.
```
use the following command to install Flask:
$  pip install Flask
```

### Flask - Sqlalchemy
```
use the following command to install Flask Sqlalchemy
$ pip install flask-sqlalchemy
```

### Flask - RESTful
**Flask-RESTful** is an extension for Flask that adds support for quickly building REST APIs. It is a lightweight abstraction that works with your existing ORM/libraries.
```
use the following command to install Flask restful
$ pip install flask-restful
```

### Flask marshmallow
Flask-Marshmallow is a thin integration layer for flask(a Python web framework) and marshmallow(an object serialization/deserialization library)
```
use the following command to install Flask marshmallow
$ pip install flask-marshmallow
```

### Flask jwt extended
```
use the following command to install Flask jwt extended
$ pip install flask-jwt-extended
```

### Flask script
**Flask-Script** extension provides support for writing external scripts in Flask.
```
$ pip install Flask-Script
```

### Flask Migrate
**Flask-Migrate** is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface.
```
use the following command to install Flask Migrate
$ pip install Flask-Migrate
```

#### Migration Commands
```
create a migration repository with the following command
$ flask db init

generate an initial migration
$ flask db migrate -m "Initial migration."

apply the migration to the database
$ flask db upgrade
```
Then each time the database models change repeat the **migrate** and **upgrade** commands.
```
To see all the commands that are available run this command
$ flask db --help
```
we can add new column in table using migration commands without losing any data and also we can create table or update table without dropping all the tables.

### Create Database
```
$ from app import db
$ from app.models import user
$ from app.models import account
$ from app.models import transaction
$ from app.models import tokenblocklist
$ db.create_all()
```
If we want to add new column in table then we have to drop all table with losing data. 

### Run project
```
$ python run.py
```
### POSTMAN Collections
[POSTMAN API](https://www.getpostman.com/collections/73332f547b6b0b6c18d5)
