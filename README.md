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

### Virtual Environment
#### Installing virtualenv
virtualenv is used to manage Python packages for different projects.You can install virtualenv using pip.
```
$ python3 -m pip install --user virtualenv
```
#### Create an environment
Create a project folder and a venv folder within:
```
$ mkdir bank-system
$ cd bank-system
$ python3 -m venv bank_env
```
#### Activate the environment
Before you can start installing or using packages in your virtual environment you’ll need to activate it. 
```
$ source bank_env/bin/activate
```
#### Leaving the virtual environment
f you want to switch projects or otherwise leave your virtual environment, simply run:
```
$ deactivate
```
### Using requirements files
Pip can export a list of all installed packages and their versions using the freeze command:
```
$ pip freeze > requirement.txt
```
Instead of installing packages individually, pip allows you to declare all dependencies in a Requirements File.
```
$ pip install -r requirement.txt
```

#### Migration Commands
For migration commands we need to install flask-script and flask-migrate
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