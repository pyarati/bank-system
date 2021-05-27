from app.models.account import AccountType
from app import db
from app import app1
from flask_script import Manager
from app import manager
from seed import seed


@manager.command
def seed():
    seed()
    print("Seed Data Loaded.")


if __name__ == "__main__":
    manager.run()
