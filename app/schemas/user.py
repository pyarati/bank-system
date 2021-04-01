from marshmallow import fields
from app import ma
from marshmallow.validate import Length, Range, Regexp


string_mobile_number = "[7-9][0-9]{9}"
string_email_id = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
string_password = "^[a-zA-Z0-9!@#\$%\^\&*_=+-]{8,12}$"


# Define schema for user
class UserSchema(ma.Schema):
    id = fields.Integer(required=True)
    first_name = fields.String(required=True, validate=Length(min=4, max=250))
    last_name = fields.String(required=True, validate=Length(min=4, max=250))
    address = fields.String(required=True, validate=Length(min=3, max=250))
    mobile_number = fields.String(required=True, validate=Regexp(string_mobile_number))
    email_id = fields.Email(required=True, validate=Regexp(string_email_id))
    password = fields.String(required=True, validate=Regexp(string_password))
    is_deleted = fields.Integer()
    user_type_id = fields.Integer(required=True, validate=Range(min=1))

    class Meta:
        fields = ("id", "first_name", "last_name", "address", "mobile_number", "email_id", "password", "user_type_id")


load_only = ["password", "is_deleted", "user_type_id"]
user_schema = UserSchema(load_only=load_only)
users_schema = UserSchema(load_only=load_only, many=True)


# Define schema for user type
class UserTypeSchema(ma.Schema):
    id = fields.Integer(required=True)
    user_type = fields.String(required=True, validate=Length(min=3, max=250))

    class Meta:
        fields = ("id", "user_type")


user_type_schema = UserTypeSchema()
users_type_schema = UserTypeSchema(many=True)
