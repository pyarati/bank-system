from app import db
from app.common.log import logger
from app.models.user import User, UserType
from flask import request
from flask_restplus import Resource
from app.schemas.user import user_schema, users_schema, user_type_schema, users_type_schema
from app.common.response_genarator import ResponseGenerator
from http import HTTPStatus
from app.common.custom_exception import UserObjectNotFound, UserTypeObjectNotFound
from flask_jwt_extended import jwt_required
import bcrypt


def is_email_id_exists(email_id):
    return User.query.filter(User.email_id == email_id).first() is not None


def is_mobile_number_exists(mobile_number):
    if User.query.filter(User.mobile_number == mobile_number).first():
        return True


class UserResources(Resource):
    def post(self):
        """
            This is POST API
            Create a new user
            parameters:
                first_name: string
                last_name: string
                address: string
                mobile_number: string
                email_id: string
                password: integer
                is_deleted: integer
                user_type_id: integer
            responses:
                404:
                    description: User does not exist
                200:
                    description: Users record inserted successfully
                    schema:
                        UserSchema
        """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = user_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            if is_email_id_exists(data['email_id']):
                logger.error("Missing or sending incorrect data to create an activity"
                             "Duplicate email id")
                response = ResponseGenerator(data={},
                                             message="Missing or sending incorrect data to create an activity."
                                                     "Duplicate email id.",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            if is_mobile_number_exists(data['mobile_number']):
                logger.error("Missing or sending incorrect data to create an activity"
                             "Duplicate mobile number")
                response = ResponseGenerator(data={},
                                             message="Missing or sending incorrect data to create an activity."
                                                     "Duplicate mobile number.",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            # get user type details
            user_type = UserType.query.filter(UserType.id == data['user_type_id']).first()
            if not user_type:
                raise UserTypeObjectNotFound("Invalid user Type id")

            try:
                user_data = User(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    address=data['address'],
                    mobile_number=data['mobile_number'],
                    email_id=data['email_id'],
                    password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()),
                    is_deleted=0,
                    user_type_id=data['user_type_id'])
            except KeyError as err:
                response = ResponseGenerator(data={},
                                             message="Column '{}' cannot be null".format(err.args[0]),
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.success_response()

            db.session.add(user_data)
            db.session.commit()
            result = user_schema.dump(user_data)

            logger.info("Response for post request for user {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Users record inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()

        except UserObjectNotFound:
            logger.exception("User does not exist")
            response = ResponseGenerator(data={},
                                         message="User does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except UserTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()

    @jwt_required()
    def get(self):
        """
             This is GET API
             parameters:
                id:int
                first_name: string
                last_name: string
                address: string
                mobile_number: string
                email_id: string
                password: int
                is_deleted: int
                user_type_id: int
             responses:
                404:
                    description: User does not exist
                200:
                    description: Users list return successfully
                    schema:
                        UserSchema
        """
        try:
            users = User.query.filter(User.is_deleted == 0)
            if users.count() == 0:
                raise UserObjectNotFound("User does not exist")

            email_id = request.args.get('email_id')
            if email_id:
                users = users.filter_by(email_id=email_id)

            result = users_schema.dump(users)

            logger.info("Response for get request for user list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Users list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except UserObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()


class UserResourcesId(Resource):
    @jwt_required()
    def get(self, user_id):
        """
            This is GET API
            Call this api passing a user id
            parameters:

                id:int
                first_name: string
                last_name: string
                address: string
                mobile_number: string
                email_id: string
                password: int
                is_deleted: int
                user_type_id: int
            responses:
                404:
                    description: User with this id does not exist
                200:
                    description: User with this id return successfully
                    schema:
                        UserSchema
        """
        try:
            user = User.query.filter(User.id == user_id, User.is_deleted == 0).first()
            if not user:
                raise UserObjectNotFound("User with this id does not exist")

            result = user_schema.dump(user)

            logger.info("Response for get with id request for user {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="User with this id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except UserObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()

    @jwt_required()
    def put(self, user_id):
        """
            This is PUT API
            Call this api passing a user id
            parameters:
                id:int
                first_name: string
                last_name: string
                address: string
                mobile_number: string
                email_id: string
                password: int
                is_deleted: int
                user_type_id: int
            responses:
                404:
                    description: User with this id does not exist
                200:
                    description: User with this id updated successfully
                    schema:
                        UserSchema
        """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = user_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            if data.get('email_id') and is_email_id_exists(data.get('email_id')):
                logger.error("Missing or sending incorrect data to create an activity."
                             "Duplicate email id")
                response = ResponseGenerator(data={},
                                             message="Missing or sending incorrect data to create an activity."
                                                     "Duplicate email id",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            if data.get('mobile_number') and is_mobile_number_exists(data.get('mobile_number')):
                logger.error("Missing or sending incorrect data to create an activity"
                             "Duplicate mobile number")
                response = ResponseGenerator(data={},
                                             message="Missing or sending incorrect data to create an activity."
                                                     "Duplicate mobile number",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            user = User.query.filter(User.id == user_id, User.is_deleted == 0).first()
            if not user:
                raise UserObjectNotFound("User with this id does not exist")

            if data.get('password'):
                hashed = bcrypt.hashpw(data.get('password', user.password).encode('utf-8'), bcrypt.gensalt())
                user.password = hashed

            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.address = data.get('address', user.address)
            user.mobile_number = data.get('mobile_number', user.mobile_number)
            user.email_id = data.get('email_id', user.email_id)
            user.user_type_id = data.get('user_type_id', user.user_type_id)

            db.session.commit()
            result = user_schema.dump(user)

            logger.info("Response for put request for user {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="User with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except UserObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()

    @jwt_required()
    def delete(self, user_id):
        """
            This is DELETE API
            Call this api passing a user id
            parameters:
                id:int
                first_name: string
                last_name: string
                address: string
                mobile_number: string
                email_id: string
                password: int
                is_deleted: int
                user_type_id: int
            responses:
                404:
                    description: User with this id does not exist
                200:
                    description: User with this id deleted successfully
                    schema:
                        UserSchema
        """
        try:
            user = User.query.filter(User.id == user_id, User.is_deleted == 0).first()
            if not user:
                raise UserObjectNotFound("User with this id not valid")

            user.is_deleted = 1
            db.session.commit()

            logger.info("Response for delete request for user: User deleted successfully")

            return "User with this id deleted successfully"
        except UserObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()


class UserTypeResource(Resource):
    @jwt_required()
    def post(self):
        """
            This is DELETE API
            parameters:
                user_type: string
            responses:
                404:
                    description: User type does not exist
                200:
                    description: User type record inserted successfully
                    schema:
                        UserTypeSchema
        """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = user_type_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()
            try:
                user_type_data = UserType(
                    user_type=data['user_type'])
            except KeyError as err:
                response = ResponseGenerator(data={},
                                             message="Column '{}' cannot be null".format(err.args[0]),
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.success_response()

            if user_type_data.user_type.lower() not in ["customer", "admin", "other"]:
                raise UserTypeObjectNotFound("Please insert correct user type")

            db.session.add(user_type_data)
            db.session.commit()
            result = user_type_schema.dump(user_type_data)

            logger.info("Response for post request for user type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="User type record inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except UserTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()

    @jwt_required()
    def get(self):
        """
            This is GET API
            parameters:
                id:int
                user_type: string
            responses:
                404:
                    description: User type does not exist
                200:
                    description: Users type list return successfully
                    schema:
                        UserTypeSchema
        """
        try:
            users_type_data = UserType.query.all()
            if not users_type_data:
                raise UserTypeObjectNotFound("Users type does not exit")

            result = users_type_schema.dump(users_type_data)

            logger.info("Response for get request for user type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Users type list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except UserTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()


class UserTypeResourceId(Resource):
    @jwt_required()
    def get(self, user_type_id):
        """
            This is GET API
            Call this api passing a user type id
            parameters:
                id:int
                user_type: string
            responses:
                404:
                    description: User type with this id does not exist
                200:
                    description: Users type with this id return successfully
                    schema:
                       UserTypeSchema
        """
        try:
            user_type_data = UserType.query.filter(UserType.id == user_type_id).first()
            if not user_type_data:
                raise UserTypeObjectNotFound("Users type with this id does not exit")

            result = user_type_schema.dump(user_type_data)

            logger.info("Response for get with id request for user type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="User type id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except UserTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()

    @jwt_required()
    def put(self, user_type_id):
        """
            This is PUT API
            Call this api passing a user type id
            parameters:
                id:int
                user_type: string
            responses:
                404:
                    description: User type with this id does not exist
                200:
                    description: User type with this id updated successfully
                    schema:
                        UserTypeSchema
        """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = user_type_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            user_type_data = UserType.query.filter(UserType.id == user_type_id).first()
            if not user_type_data:
                raise UserTypeObjectNotFound("User type with this id does not exist")

            user_type_data.user_type = data.get('user_type', user_type_data.user_type)
            db.session.commit()
            result = user_type_schema.dump(user_type_data)

            logger.info("Response for put with id request for user type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Users type record updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except UserTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)

        return response.error_response()
