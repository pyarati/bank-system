from marshmallow import fields
from app import ma
from marshmallow.validate import Length, Regexp

string_pattern = "^[a-zA-Z ]*$"


class AccountTransactionDetailsSchema(ma.Schema):
    id = fields.Integer(required=True)
    transaction_amount = fields.Integer(required=True)
    transaction_status = fields.String(required=True)
    bank_account_id = fields.Integer(required=True)
    transaction_type_id = fields.Integer(required=True)
    fund_transfer_id = fields.Integer(required=False)
    fund_transfer_info = fields.String(required=False, validate=Regexp(string_pattern))

    class Meta:
        fields = (
            "id", "transaction_amount", "transaction_status", "bank_account_id",
            "transaction_type_id", "fund_transfer_id", "fund_transfer_info"
        )


account_transaction_details_schema = AccountTransactionDetailsSchema()
accounts_transaction_details_schema = AccountTransactionDetailsSchema(many=True)


class TransactionTypeSchema(ma.Schema):
    id = fields.Integer(required=True)
    transaction_type = fields.String(required=True, validate=(Length(min=3, max=250), Regexp(string_pattern)))

    class Meta:
        fields = ("id", "transaction_type")


transaction_type_schema = TransactionTypeSchema()
transactions_type_schema = TransactionTypeSchema(many=True)


class FundTransferSchema(ma.Schema):
    id = fields.Integer(required=True)
    from_account = fields.String(required=True, validate=Length(equal=8))
    to_account = fields.String(required=True, validate=Length(equal=8))
    transaction_amount = fields.Integer()

    class Meta:
        fields = ("id", "from_account", "to_account", "transaction_amount")


fund_transfer_schema = FundTransferSchema()
funds_transfer_schema = FundTransferSchema(many=True)
