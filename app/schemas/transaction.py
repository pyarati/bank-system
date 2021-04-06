from marshmallow import fields
from app import ma
from marshmallow.validate import Length


class AccountTransactionDetailsSchema(ma.Schema):
    id = fields.Integer(required=True)
    transaction_amount = fields.Integer(required=True)
    bank_account_id = fields.Integer(required=True)
    transaction_type_id = fields.Integer(required=True)
    fund_transfer_id = fields.Integer(required=True)

    class Meta:
        fields = ("id", "transaction_amount", "bank_account_id", "transaction_type_id", "fund_transfer_id")


account_transaction_details_schema = AccountTransactionDetailsSchema()
accounts_transaction_details_schema = AccountTransactionDetailsSchema(many=True)


class TransactionTypeSchema(ma.Schema):
    id = fields.Integer(required=True)
    transaction_type = fields.String(required=True, validate=Length(min=3, max=250))

    class Meta:
        fields = ("id", "transaction_type")


transaction_type_schema = TransactionTypeSchema()
transactions_type_schema = TransactionTypeSchema(many=True)


class FundTransferSchema(ma.Schema):
    id = fields.Integer(required=True)
    source = fields.String(required=True, validate=Length(min=3, max=250))
    destination = fields.String(required=True, validate=Length(min=3, max=250))

    class Meta:
        fields = ("id", "source", "destination")


fund_transfer_schema = FundTransferSchema()
funds_transfer_schema = FundTransferSchema(many=True)
