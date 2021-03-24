from marshmallow import fields
from app import ma
from marshmallow.validate import Length, Range


class BankAccountSchema(ma.Schema):
    account_number = fields.Integer(required=True, validate=Length(max=16))
    is_active = fields.String(required=True)
    deleted = fields.String(required=True)
    user_id = fields.Integer(required=True, validate=Range(min=1))
    branch_id = fields.Integer(required=True, validate=Range(min=1))
    account_type_id = fields.Integer(required=True, validate=Range(min=1))

    class Meta:
        fields = ("account_number", "is_active", "deleted", "user_id", "branch_id", "account_type_id")


bank_account_schema = BankAccountSchema()
bank_accounts_schema = BankAccountSchema(many=True)


class AccountTypeSchema(ma.Schema):
    id = fields.Int()
    account_type = fields.Str()

    class Meta:
        fields = ("id", "account_type")


account_type_schema = AccountTypeSchema()
accounts_type_schema = AccountTypeSchema(many=True)


class BranchDetailsSchema(ma.Schema):
    id = fields.Int()
    branch_code = fields.Int()
    branch_address = fields.Str()

    class Meta:
        fields = ("id", "branch_code", "branch_address")


branch_details_schema = BranchDetailsSchema()
branchs_details_schema = BranchDetailsSchema(many=True)
