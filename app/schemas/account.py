from marshmallow import fields
from app import ma
from marshmallow.validate import Length


class BankAccountSchema(ma.Schema):
    id = fields.Integer(required=True)
    account_number = fields.String(required=True, validate=Length(equal=8))
    is_active = fields.Integer()
    is_deleted = fields.Integer()
    user_id = fields.Integer(required=True)
    branch_id = fields.Integer(required=True)
    account_type_id = fields.Integer(required=True)

    class Meta:

        fields = ("id", "account_number", "is_active", "is_deleted", "user_id", "branch_id", "account_type_id")


bank_account_schema = BankAccountSchema()
bank_accounts_schema = BankAccountSchema(many=True)


class AccountTypeSchema(ma.Schema):
    id = fields.Integer(required=True)
    account_type = fields.String(required=True, validate=Length(min=3, max=250))

    class Meta:
        fields = ("id", "account_type")


account_type_schema = AccountTypeSchema()
accounts_type_schema = AccountTypeSchema(many=True)


class BranchDetailsSchema(ma.Schema):
    id = fields.Integer(required=True)
    branch_address = fields.String(required=True, validate=Length(min=3, max=250))

    class Meta:
        fields = ("id", "branch_address")


branch_details_schema = BranchDetailsSchema()
branches_details_schema = BranchDetailsSchema(many=True)
