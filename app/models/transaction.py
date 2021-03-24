from app import db
from datetime import datetime


class TransactionType(db.Model):
    __tablename__ = 'TransactionType'
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(50), nullable=False)

    account_transaction_details = db.relationship('AccountTransactionDetails', backref='TransactionType', lazy=True)

    def __init__(self, transaction_type):
        self.transaction_type = transaction_type


class FundTransfer(db.Model):
    __tablename__ = 'FundTransfer'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)

    account_transaction_details = db.relationship('AccountTransactionDetails', backref='FundTransfer', lazy=True)

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


class AccountTransactionDetails(db.Model):
    __tablename__ = 'AccountTransactionDetails'
    id = db.Column(db.Integer, primary_key=True)
    transaction_amount = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime)

    account_number = db.Column(db.Integer, db.ForeignKey('BankAccount.account_number'), nullable=False)
    fund_id = db.Column(db.Integer, db.ForeignKey('FundTransfer.id'), nullable=False)

    def __init(self, transaction_amount, transaction_date, account_number, fund_id):
        self.transaction_amount = transaction_amount
        self.transaction_date = datetime.strptime(transaction_date, '%d%m%Y').date()
        self.account_number = account_number
        self.fund_id = fund_id
