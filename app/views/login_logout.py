from flask_restplus import Resource
from flask import request
from app.views.user import User
from app.common.response_genarator import ResponseGenerator
from app.common.log import logger
from app import db
from app import jwt
from http import HTTPStatus
from app.common.custom_exception import UserObjectNotFound, PasswordWrong
from app.models.tokenblocklist import TokenBlockList
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import datetime, timezone
import bcrypt


class Login(Resource):
    def post(self):
        """
              This is POST API
             parameters:
                 email_id: String
                 password: String
             responses:
                 404:
                     description: User email_id and password not exist
                 201:
                     description: Successfully logged in
                 400:
                     description: Bad request
        """
        try:
            email_id = request.json.get("email_id")
            password = request.json.get("password")
            if not email_id:
                logger.warning("Missing email id")
                response = ResponseGenerator(data={},
                                             message="Missing email id, Please enter email id",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()
            if not password:
                logger.warning("Missing password")
                response = ResponseGenerator(data={},
                                             message="Missing password, Please enter password",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            user_data = User.query.filter_by(email_id=email_id).first()
            if not user_data:
                raise UserObjectNotFound("User not found")

            if not bcrypt.checkpw(password.encode('utf-8'), user_data.password.encode('utf-8')):
                raise PasswordWrong("Password is wrong")

            access_token = create_access_token(identity={"email_id": email_id, "password": password})
            logger.info("Successfully logged in")
            response = ResponseGenerator(data={"access_token": access_token},
                                         message="Successfully logged in",
                                         success=True,
                                         status=HTTPStatus.CREATED)
            return response.success_response()
        except UserObjectNotFound as err:
            logger.info(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=True,
                                         status=HTTPStatus.NOT_FOUND)
        except PasswordWrong as err:
            logger.info(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=True,
                                         status=HTTPStatus.NOT_FOUND)
        except Exception as err:
            logger.info(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=True,
                                         status=HTTPStatus.BAD_REQUEST)
        return response.success_response()


class Logout(Resource):
    @jwt_required()
    def delete(self):
        try:
            jti = get_jwt()["jti"]
            now = datetime.now(timezone.utc)
            db.session.add(TokenBlockList(jti=jti, created_at=now))
            db.session.commit()
            logger.info("Logged out")
            response = ResponseGenerator(data={},
                                         message="logged out",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except Exception as err:
            logger.info(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=True,
                                         status=HTTPStatus.BAD_REQUEST)
        return response.success_response()
