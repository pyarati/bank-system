from app import db


class BankAccount(db.Model):
    __tablename__ = 'BankAccount'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(8), unique=True)
    is_active = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)
    account_balance = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('BranchDetails.id'), nullable=False)
    account_type_id = db.Column(db.Integer, db.ForeignKey('AccountType.id'), nullable=False)

    account_transaction_details = db.relationship('AccountTransactionDetails', backref='BankAccount', lazy=True)

    def __init__(self, account_number, is_active, is_deleted, account_balance, user_id, branch_id, account_type_id):
        self.account_number = account_number
        self.is_active = is_active
        self.is_deleted = is_deleted
        self.account_balance = account_balance
        self.user_id = user_id
        self.branch_id = branch_id
        self.account_type_id = account_type_id


class AccountType(db.Model):
    __tablename__ = 'AccountType'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(50), nullable=False)

    bank_account = db.relationship('BankAccount', backref='AccountType', lazy=True)

    def __init__(self, account_type):
        self.account_type = account_type


class BranchDetails(db.Model):
    __tablename__ = 'BranchDetails'
    id = db.Column(db.Integer, primary_key=True)
    branch_address = db.Column(db.String(50), nullable=False)

    bank_account = db.relationship('BankAccount', backref='BranchDetails', lazy=True)

    def __init__(self, branch_address):
        self.branch_address = branch_address
