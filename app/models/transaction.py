from app import db


class AccountTransactionDetails(db.Model):
    __tablename__ = 'AccountTransactionDetails'
    id = db.Column(db.Integer, primary_key=True)
    transaction_amount = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, server_default=db.func.now())
    transaction_status = db.Column(db.String(50))
    bank_account_id = db.Column(db.Integer, db.ForeignKey('BankAccount.id'), nullable=False)
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('TransactionType.id'), nullable=False)
    fund_transfer_id = db.Column(db.Integer, db.ForeignKey('FundTransfer.id'), nullable=False)
    fund_transfer_info = db.Column(db.String(50))

    def __init__(self, transaction_amount, transaction_status,
                 bank_account_id, transaction_type_id, fund_transfer_id, fund_transfer_info):
        self.transaction_amount = transaction_amount
        self.transaction_status = transaction_status
        self.bank_account_id = bank_account_id
        self.transaction_type_id = transaction_type_id
        self.fund_transfer_id = fund_transfer_id
        self.fund_transfer_info = fund_transfer_info


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
    from_account = db.Column(db.String(8), nullable=False)
    to_account = db.Column(db.String(8), nullable=True)

    account_transaction_details = db.relationship('AccountTransactionDetails', backref='FundTransfer', lazy=True)

    def __init__(self, from_account, to_account):
        self.from_account = from_account
        self.to_account = to_account
