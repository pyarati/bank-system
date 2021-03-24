from app import db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, )
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    address = db.Column(db.String(50), unique=False, nullable=False)
    mobile_number = db.Column(db.String(10), unique=True, nullable=False)
    email_id = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    is_deleted = db.Column(db.Integer)

    user_type_id = db.Column(db.Integer, db.ForeignKey('UserType.id'), nullable=False)

    # bank_account = db.relationship('BankAccount', backref='User', lazy=True)

    def __init__(self, first_name, last_name, address, mobile_number, email_id, password, is_deleted, user_type_id):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.mobile_number = mobile_number
        self.email_id = email_id
        self.password = password
        self.is_deleted = is_deleted
        self.user_type_id = user_type_id


class UserType(db.Model):
    __tablename__ = 'UserType'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50), nullable=False)

    user_profile = db.relationship('User', backref='UserType', lazy=True)

    def __init__(self, user_type):
        self.user_type = user_type
