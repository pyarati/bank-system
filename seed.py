from app.models.account import AccountType
from app import db
from app import app1
from flask_script import Manager

manager = Manager(app1)

@manager.command
def seed():
    db.session.add(AccountType(account_type="Saving"))
    db.session.add(AccountType(account_type="Current"))
    db.session.commit()
