from app import db
from app.common.log import logger
from app.models.account import BankAccount
from app.models.user import User, UserType
from flask import request
from flask_restplus import Resource
from app.schemas.user import user_schema, users_schema, user_type_schema, users_type_schema
from app.common.response_genarator import ResponseGenerator
from http import HTTPStatus
from sqlalchemy.orm.exc import NoResultFound


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
                200:
                    description: Users record inserted successfully
                    schema:
                        UserSchema
        """
        # retrieve body data from input JSON
        data = request.get_json()
        errors = user_schema.validate(data, partial=True)

        if errors:
            logger.error("Missing or sending incorrect data to create an activity")
            response = ResponseGenerator(data={},
                                         message="Missing or sending incorrect data to create an activity",
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

        user_data = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            mobile_number=data['mobile_number'],
            email_id=data['email_id'],
            password=data['password'],
            is_deleted=0,
            user_type_id=data['user_type_id'])

        db.session.add(user_data)
        db.session.commit()
        result = user_schema.dump(user_data)

        logger.info("Response for post request for user {}".format(result))
        response = ResponseGenerator(data=result,
                                     message="Users record inserted successfully",
                                     success=True,
                                     status=HTTPStatus.OK)
        return response.success_response()

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
                raise NoResultFound

            result = users_schema.dump(users)

            logger.info("Response for get request for user list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Users list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("User does not exist")
            response = ResponseGenerator(data={},
                                         message="User does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class UserResourcesId(Resource):
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
                raise NoResultFound

            result = user_schema.dump(user)

            logger.info("Response for get with id request for user {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="User with this id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("User with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="User with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

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
                logger.error("Missing or sending incorrect data to create an activity")
                response = ResponseGenerator(data={},
                                             message="Missing or sending incorrect data to create an activity",
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
                raise NoResultFound

            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.address = data.get('address', user.address)
            user.mobile_number = data.get('mobile_number', user.mobile_number)
            user.email_id = data.get('email_id', user.email_id)
            user.password = data.get('password', user.password)
            user.user_type_id = data.get('user_type_id', user.user_type_id)

            db.session.commit()
            result = user_schema.dump(user)

            logger.info("Response for put request for user {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="User with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("User with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="User with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

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
                raise NoResultFound

            user.is_deleted = 1

            db.session.commit()

            logger.info("Response for delete request for user: User deleted successfully")

            return "User with this id deleted successfully"
        except NoResultFound:
            logger.exception("Response for delete request for user: User with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="User with this id not valid",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class UserTypeResource(Resource):
    def post(self):
        """
            This is DELETE API
            parameters:
                user_type: string
            responses:
                200:
                    description: User type record inserted successfully
                    schema:
                        UserTypeSchema
        """
        # retrieve body data from input JSON
        data = request.get_json()
        user_type_data = UserType(
            user_type=data['user_type'])

        db.session.add(user_type_data)
        db.session.commit()
        result = user_type_schema.dump(user_type_data)
        logger.info("Response for post request for user type {}".format(result))
        response = ResponseGenerator(data=result,
                                     message="User type record inserted successfully",
                                     success=True,
                                     status=HTTPStatus.OK)
        return response.success_response()

    def get(self):
        """
            This is GET API
            parameters:
                id:int
                user_type: string
            responses:
                404:
                    description: User with this id does not exist
                200:
                    description: Users type list return successfully
                    schema:
                        UserTypeSchema
        """
        try:
            users_type_data = UserType.query.all()
            if not users_type_data:
                raise NoResultFound

            result = users_type_schema.dump(users_type_data)

            logger.info("Response for get request for user type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Users type list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("User type does not exist")
            response = ResponseGenerator(data={},
                                         message="Users type does not exit",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class UserTypeResourceId(Resource):
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
                    description: Users type id return successfully
                    schema:
                       UserTypeSchema
        """
        try:
            user_type_data = UserType.query.filter(UserType.id == user_type_id).first()
            if not user_type_data:
                raise NoResultFound
            result = user_type_schema.dump(user_type_data)

            logger.info("Response for get with id request for user type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="User type id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("User type with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Users type with this id does not exit",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def put(self, user_type_id):
        """
            This is PUT API
            Call this api passing a user type id
            parameters:
                id:int
                user_type: string
            responses:
                404:
                    description: User with this id does not exist
                200:
                    description: User record updated successfully
                    schema:
                        UserTypeSchema
        """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = user_type_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data to create an activity")
                response = ResponseGenerator(data={},
                                             message="Missing or sending incorrect data to create an activity",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            user_type_data = UserType.query.filter(UserType.id == user_type_id).first()
            if not user_type_data:
                raise NoResultFound

            user_type_data.user_type = data.get('user_type', user_type_data.user_type)
            db.session.commit()
            result = user_type_schema.dump(user_type_data)

            logger.info("Response for put with id request for user type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Users type record updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("User type with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Users type not valid",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def delete(self, user_type_id):
        """
            This is DELETE API
            Call this api passing a user type id
            parameters:
                id:int
                user_type: string
            responses:
                404:
                    description: User type with this id does not exist
                200:
                    description: User type record deleted successfully
                    schema:
                        UserTypeSchema
        """


        try:
            user_type = UserType.query.filter(UserType.id == user_type_id).first()
            db.session.delete(user_type)
            db.session.commit()

            logger.info("Response for delete request for user type: User type deleted successfully")

            return "User type record deleted successfully"
        except Exception:
            logger.exception("Response for delete request for user type: User type with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Users type with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()
