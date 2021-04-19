from app import db
from app.common.log import logger
from app.models.account import BankAccount, BranchDetails, AccountType
from flask import request
from flask_restplus import Resource
from app.schemas.account import bank_account_schema, bank_accounts_schema, account_type_schema, accounts_type_schema, branch_details_schema, branches_details_schema
from app.common.response_genarator import ResponseGenerator
from http import HTTPStatus
import random
from app.common.custom_exception import BankAccountObjectNotFound, AccountTypeObjectNotFound, BranchDetailsObjectNotFound


class BankAccountResource(Resource):
    def post(self):
        """
             This is POST API
             Create a new bank account
             parameters:
                 account_number: Integer
                 is_active: Integer
                 is_deleted: Integer
                 user_id: Integer
                 account_type_id: Integer
                 branch_id: Integer
             responses:
                 404:
                     description: Bank account does not exits
                 200:
                     description: Bank account record inserted successfully
                     schema:
                         BankAccountSchema
         """
        # retrieve body data from input JSON
        try:
            data = request.get_json()
            errors = bank_account_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            branch_id = data['branch_id']
            zero_filled_number = str(branch_id)
            branch_id = zero_filled_number.zfill(3)
            code = random.randint(10000, 99999)
            account_number = f'{branch_id}{code}'

            bank_account_data = BankAccount(
                account_number=account_number,
                is_active=1,
                is_deleted=0,
                account_balance=data['account_balance'],
                user_id=data['user_id'],
                account_type_id=data['account_type_id'],
                branch_id=branch_id)

            if bank_account_data.account_balance <= 1000:
                raise BankAccountObjectNotFound("Minimum balances required while creating account")

            db.session.add(bank_account_data)
            db.session.commit()
            result = bank_account_schema.dump(bank_account_data)
            logger.info("Response for get request for bank account list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Bank account list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def get(self):
        """
             This is GET API
             parameters:
                 account_number: Integer
                 is_active: Integer
                 is_deleted: Integer
                 user_id: Integer
                 account_type_id: Integer
                 branch_id: Integer
             responses:
                 404:
                     description: Bank account does not exist
                 200:
                     description: Bank account list return successfully
                     schema:
                         BankAccountSchema
         """
        try:
            bank_account_data = BankAccount.query.filter(BankAccount.is_deleted == 0)
            if bank_account_data.count() == 0:
                raise BankAccountObjectNotFound("Bank account does not exist")

            result = bank_accounts_schema.dump(bank_account_data)

            logger.info("Response for get request for bank account list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Bank account list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class BankAccountResourceId(Resource):
    def get(self, bank_account_id):
        """
             This is GET API
             Call this api passing a bank account id
             parameters:
                 account_number: Integer
                 is_active: Integer
                 is_deleted: Integer
                 user_id: Integer
                 account_type_id: Integer
                 branch_id: Integer
             responses:
                 404:
                     description: Bank account with this id does not exist
                 200:
                     description: Bank account with this id return successfully
                     schema:
                         BankAccountSchema
         """
        try:
            bank_account_data = BankAccount.query.filter(BankAccount.id == bank_account_id,
                                                         BankAccount.is_deleted == 0).first()
            if not bank_account_data:
                raise BankAccountObjectNotFound("Bank account does not exist")

            result = bank_account_schema.dump(bank_account_data)
            logger.info("Response for get request for bank account list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Bank account list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def put(self, bank_account_id):
        """
             This is PUT API
             Call this api passing a bank account id
             parameters:
                 account_number: Integer
                 is_active: Integer
                 is_deleted: Integer
                 user_id: Integer
                 account_type_id: Integer
                 branch_id: Integer
             responses:
                 404:
                     description: Bank account with this id does not exist
                 200:
                     description: Bank account with this id updated successfully
                     schema:
                         BankAccountSchema
         """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = bank_account_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            bank_account_data = BankAccount.query.filter(BankAccount.id == bank_account_id,
                                                         BankAccount.is_deleted == 0).first()
            if not bank_account_data:
                raise BankAccountObjectNotFound("Bank account with this id does not exist")

            bank_account_data.user_id = data.get('user_id', bank_account_data.user_id)
            bank_account_data.branch_id = data.get('branch_id', bank_account_data.branch_id)
            bank_account_data.account_type_id = data.get('account_type_id', bank_account_data.account_type_id)

            db.session.commit()
            result = bank_account_schema.dump(bank_account_data)

            logger.info("Response for put with id request for user type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Bank account with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()

        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def delete(self, bank_account_id):
        """
             This is DELETE API
             Call this api passing a bank account id
             parameters:
                 account_number: Integer
                 is_active: Integer
                 is_deleted: Integer
                 user_id: Integer
                 account_type_id: Integer
                 branch_id: Integer
             responses:
                 404:
                     description: Bank account with this id does not exist
                 200:
                     description: Bank account with this id deleted successfully
                     schema:
                         BankAccountSchema
         """
        try:
            bank_account_data = BankAccount.query.filter(BankAccount.id == bank_account_id,
                                                         BankAccount.is_deleted == 0).first()
            if not bank_account_data:
                raise BankAccountObjectNotFound("Bank account with this id does not exit")

            bank_account_data.is_deleted = 1
            db.session.commit()

            logger.info("Response for delete request for user: Bank account deleted successfully")

            return "Bank account with this id deleted successfully"
        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class AccountTypeResource(Resource):
    def post(self):
        """
             This is POST API
             parameters:
                 account_type: String
             responses:
                 404:
                     description: Account type does not exist
                 200:
                     description: Account type record inserted successfully
                     schema:
                         AccountTypeSchema
         """
        try:
            data = request.get_json()
            errors = account_type_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            account_type_data = AccountType(
                account_type=data['account_type'])

            db.session.add(account_type_data)
            db.session.commit()
            result = account_type_schema.dump(account_type_data)
            logger.info("Response for post request for account type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account type list inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except AccountTypeObjectNotFound:
            logger.exception("Account type does not exist")
            response = ResponseGenerator(data={},
                                         message="Account type does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def get(self):
        """
             This is GET API
             parameters:
                 account_type: String
             responses:
                 404:
                     description: Account type does not exist
                 200:
                     description: Account type list return successfully
                     schema:
                         AccountTypeSchema
         """
        try:
            account_type_data = AccountType.query.all()
            if not account_type_data:
                raise AccountTypeObjectNotFound("Account type does not exist")

            result = accounts_type_schema.dump(account_type_data)

            logger.info("Response for get request for account type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account type list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except AccountTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class AccountTypeResourceId(Resource):
    def get(self, account_type_id):
        """
             This is GET API
             Call this api passing a account type id
             parameters:
                 account_type: String
             responses:
                 404:
                     description: Account type with this id does not exist
                 200:
                     description: Account type with this id return successfully
                     schema:
                         AccountTypeSchema
         """
        try:
            account_type_data = AccountType.query.filter(AccountType.id == account_type_id).first()
            if not account_type_data:
                raise AccountTypeObjectNotFound("Account type with this id does not exist")

            result = account_type_schema.dump(account_type_data)

            logger.info("Response for get with id request for account type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="account type with this  id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except AccountTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def put(self, account_type_id):
        """
             This is PUT API
             Call this api passing a account type id
             parameters:
                 account_type: String
             responses:
                 404:
                     description: Account type with this id does not exist
                 200:
                     description: Account type with this id updated successfully
                     schema:
                         AccountTypeSchema
         """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = account_type_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            account_type_data = AccountType.query.filter(AccountType.id == account_type_id).first()
            if not account_type_data:
                raise AccountTypeObjectNotFound("Account type with this id does not exist")

            account_type_data.account_type = data.get('account_type', account_type_data.account_type)
            db.session.commit()
            result = account_type_schema.dump(account_type_data)

            logger.info("Response for put with id request for account type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account type with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except AccountTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class BranchDetailsResource(Resource):
    def post(self):
        """
             This is POST API
             parameters:
                 branch_code: String
                 branch_address: String
             responses:
                 404:
                     description: Branch details does not exist
                 200:
                     description: Branch details record inserted successfully
                     schema:
                         BranchDetailsSchema
         """
        try:
            data = request.get_json()
            errors = branch_details_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            branch_details_data = BranchDetails(
                branch_address=data['branch_address'])

            db.session.add(branch_details_data)
            db.session.commit()
            result = branch_details_schema.dump(branch_details_data)
            logger.info("Response for post request for branch details {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Branch details record inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BranchDetailsObjectNotFound:
            logger.exception("Branch details does not exist")
            response = ResponseGenerator(data={},
                                         message="Branch details does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def get(self):
        """
             This is GET API
             parameters:
                 branch_code: String
                 branch_address: String
             responses:
                 404:
                     description: Branch details does not exist
                 200:
                     description: Branch details list return successfully
                     schema:
                         BranchDetailsSchema
         """
        try:
            branch_details_data = BranchDetails.query.all()
            if not branch_details_data:
                raise BranchDetailsObjectNotFound("Branch details does not exist")

            result = branches_details_schema.dump(branch_details_data)

            logger.info("Response for get request for branch details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Branch details list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BranchDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class BranchDetailsResourceId(Resource):
    def get(self, branch_details_id):
        """
             This is GET API
             Call this api passing a branch details id
             parameters:
                 branch_code: String
                 branch_address: String
             responses:
                 404:
                     description: Branch details with this id does not exist
                 200:
                     description: Branch details with this id return successfully
                     schema:
                         BranchDetailsSchema
         """
        try:
            branch_details_data = BranchDetails.query.filter(BranchDetails.id == branch_details_id).first()
            if not branch_details_data:
                raise BranchDetailsObjectNotFound("Branch details with this id does not exist")

            result = branch_details_schema.dump(branch_details_data)

            logger.info("Response for get with id request for branch details {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Branch details with this id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BranchDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def put(self, branch_details_id):
        """
             This is PUT API
             Call this api passing a branch details id
             parameters:
                 branch_code: String
                 branch_address: String
             responses:
                 404:
                     description: Branch details with this id does not exist
                 200:
                     description: Branch details with this id updated successfully
                     schema:
                         BranchDetailsSchema
         """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = branch_details_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            branch_details_data = BranchDetails.query.filter(BranchDetails.id == branch_details_id).first()
            if not branch_details_data:
                raise BranchDetailsObjectNotFound("Branch details with this id does not exist")

            branch_details_data.branch_address = data.get('branch_address', branch_details_data.branch_address)
            db.session.commit()
            result = branch_details_schema.dump(branch_details_data)

            logger.info("Response for put with id request for user type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Branch details with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BranchDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def delete(self, branch_details_id):
        """
             This is DELETE API
             Call this api passing a branch details id
             parameters:
                 branch_code: String
                 branch_address: String
             responses:
                 404:
                     description: Branch details with this id does not exist
                 200:
                     description: Branch details with this id deleted successfully
                     schema:
                         BranchDetailsSchema
         """
        try:
            branch_details_data = BranchDetails.query.filter(BranchDetails.id == branch_details_id).first()
            if not branch_details_data:
                raise BranchDetailsObjectNotFound("Branch details with this id does not exist")

            db.session.delete(branch_details_data)
            db.session.commit()

            logger.info("Response for delete request for branch details:"
                        "Branch details with this id deleted successfully")

            return "Branch details record deleted successfully"
        except BranchDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()
