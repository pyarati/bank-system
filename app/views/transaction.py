from app import db
from app.common.log import logger
from flask import request
from flask_restplus import Resource
from app.models.transaction import AccountTransactionDetails, TransactionType, FundTransfer
from app.schemas.transaction import account_transaction_details_schema, accounts_transaction_details_schema, transaction_type_schema, transactions_type_schema, fund_transfer_schema, funds_transfer_schema
from app.common.response_genarator import ResponseGenerator
from http import HTTPStatus
from sqlalchemy.orm.exc import NoResultFound


class AccountTransactionDetailsResource(Resource):
    def post(self):
        """
              This is POST API
              Create a new account transaction
             parameters:
                 transaction_amount: Integer
                 transaction_date: DateTime
                 bank_account_id: Integer
                 transaction_type_id: Integer
                 fund_transfer_id: Integer
             responses:
                 404:
                     description: Account transaction details does not exist
                 200:
                     description: Account transaction details record inserted successfully
                     schema:
                         AccountTransactionDetailsSchema
         """
        # retrieve body data from input JSON
        try:
            data = request.get_json()
            errors = account_transaction_details_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data to create an activity {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            bank_account_data = AccountTransactionDetails(
                transaction_amount=data['transaction_amount'],
                bank_account_id=data['bank_account_id'],
                transaction_type_id=data['transaction_type_id'],
                fund_transfer_id=data['fund_transfer_id'])

            db.session.add(bank_account_data)
            db.session.commit()
            result = account_transaction_details_schema.dump(bank_account_data)
            logger.info("Response for get request for account transaction details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details list inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Account transaction details does not exist")
            response = ResponseGenerator(data={},
                                         message="Account transaction details does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def get(self):
        """
             This is GET API
             parameters:
                 transaction_amount: Integer
                 transaction_date: DateTime
                 bank_account_id: Integer
                 transaction_type_id: Integer
                 fund_transfer_id: Integer
             responses:
                 404:
                     description: Account transaction details does not exist
                 200:
                     description: Account transaction details list return successfully
                     schema:
                         AccountTransactionDetailsSchema
         """
        try:
            account_transaction_details_data = AccountTransactionDetails.query.all()
            if not account_transaction_details_data:
                raise NoResultFound

            result = accounts_transaction_details_schema.dump(account_transaction_details_data)

            logger.info("Response for get request for account transaction details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Account transaction details does not exist")
            response = ResponseGenerator(data={},
                                         message="Account transaction details does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class AccountTransactionDetailsResourceId(Resource):
    def get(self, account_transaction_details_id):
        """
             This is GET API
             call this api passing account transaction details id
             parameters:
                 transaction_amount: Integer
                 transaction_date: DateTime
                 bank_account_id: Integer
                 transaction_type_id: Integer
                 fund_transfer_id: Integer
             responses:
                 404:
                     description: Account transaction details with this id does not exist
                 200:
                     description: Account transaction details with this id return successfully
                     schema:
                         AccountTransactionDetailsSchema
         """
        try:
            account_transaction_details_data = AccountTransactionDetails.query.filter(AccountTransactionDetails.id == account_transaction_details_id).first()
            if not account_transaction_details_data:
                raise NoResultFound

            result = account_transaction_details_schema.dump(account_transaction_details_data)

            logger.info("Response for get request for account transaction details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Account transaction details does not exist")
            response = ResponseGenerator(data={},
                                         message="Account transaction details does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def put(self, account_transaction_details_id):
        """
             This is PUT API
             Call this api passing a account transaction details id
             parameters:
                 transaction_amount: Integer
                 transaction_date: DateTime
                 bank_account_id: Integer
                 transaction_type_id: Integer
                 fund_transfer_id: Integer
             responses:
                 404:
                     description: Account transaction details with this id does not exist
                 200:
                     description: Account transaction details with this id updated successfully
                     schema:
                         AccountTransactionDetailsSchema
         """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = account_transaction_details_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data to create an activity {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            account_transaction_details_data = AccountTransactionDetails.query.filter(AccountTransactionDetails.id == account_transaction_details_id).first()
            if not account_transaction_details_data:
                raise NoResultFound

            account_transaction_details_data.transaction_amount = data.get('transaction_amount', account_transaction_details_data.transaction_amount)
            account_transaction_details_data.bank_account_id = data.get('bank_account_id', account_transaction_details_data.bank_account_id)
            account_transaction_details_data.transaction_type_id = data.get('transaction_type_id', account_transaction_details_data.transaction_type_id)
            account_transaction_details_data.fund_transfer_id = data.get('fund_transfer_id', account_transaction_details_data.fund_transfer_id)

            db.session.commit()
            result = account_transaction_details_schema.dump(account_transaction_details_data)

            logger.info("Response for put with id request for account transaction details {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()

        except NoResultFound:
            logger.exception("Account transaction details with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Account transaction details with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def delete(self, account_transaction_details_id):
        """
             This is DELETE API
             call this api passing account transaction details id
             parameters:
                 transaction_amount: Integer
                 transaction_date: DateTime
                 bank_account_id: Integer
                 transaction_type_id: Integer
                 fund_transfer_id: Integer
             responses:
                 404:
                     description: Account transaction details with this id does not exist
                 200:
                     description: Account transaction details with this id deleted successfully
                     schema:
                         AccountTransactionDetailsSchema
         """
        try:
            account_transaction_details_data = AccountTransactionDetails.query.filter(AccountTransactionDetails.id == account_transaction_details_id).first()
            db.session.delete(account_transaction_details_data)
            db.session.commit()

            logger.info("Response for delete request for account transaction details:"
                        "Account transaction details with this id deleted successfully")

            return "Account transaction details record deleted successfully"
        except Exception:
            logger.exception("Response for delete request for account transaction details:"
                             "Account transaction details with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Account transaction details with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class TransactionTypeResource(Resource):
    def post(self):
        """
             This is POST API
             parameters:
                 transaction_type: String
             responses:
                 404:
                     description: Transaction type does not exist
                 200:
                     description: Transaction type record inserted successfully
                     schema:
                         TransactionTypeSchema
         """
        try:
            data = request.get_json()
            errors = transaction_type_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data to create an activity {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            transaction_type_data = TransactionType(
                transaction_type=data['transaction_type'])

            db.session.add(transaction_type_data)
            db.session.commit()
            result = transaction_type_schema.dump(transaction_type_data)
            logger.info("Response for post request for transaction type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type list inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Transaction type does not exist")
            response = ResponseGenerator(data={},
                                         message="Transaction type does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def get(self):
        """
             This is GET API
             parameters:
                 transaction_type: String
             responses:
                 404:
                     description: Transaction type does not exist
                 200:
                     description: Transaction type list return successfully
                     schema:
                         TransactionTypeSchema
         """
        try:
            transaction_type_data = TransactionType.query.all()
            if not transaction_type_data:
                raise NoResultFound

            result = transactions_type_schema.dump(transaction_type_data)

            logger.info("Response for get request for transaction type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Transaction type does not exist")
            response = ResponseGenerator(data={},
                                         message="Transaction type does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class TransactionTypeResourceId(Resource):
    def get(self, transaction_type_id):
        """
             This is GET API
             Call this api passing a transaction type id
             parameters:
                 transaction_type: String
             responses:
                 404:
                     description: Transaction type with this id does not exist
                 200:
                     description: Transaction type with this id return successfully
                     schema:
                         TransactionTypeSchema
         """
        try:
            transaction_type_data = TransactionType.query.filter(TransactionType.id == transaction_type_id).first()
            if not transaction_type_data:
                raise NoResultFound

            result = transaction_type_schema.dump(transaction_type_data)

            logger.info("Response for get with id request for transaction type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type with this  id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Transaction type with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Transaction type with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def put(self, transaction_type_id):
        """
              This is PUT API
              Call this api passing a transaction type id
             parameters:
                 transaction_type: String
             responses:
                 404:
                     description: Transaction type with this id does not exist
                 200:
                     description: Transaction type with this id updated successfully
                     schema:
                         TransactionTypeSchema
         """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = transaction_type_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data to create an activity {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            transaction_type_data = TransactionType.query.filter(TransactionType.id == transaction_type_id).first()
            if not transaction_type_data:
                raise NoResultFound

            transaction_type_data.transaction_type = data.get('transaction_type', transaction_type_data.transaction_type)
            db.session.commit()
            result = transaction_type_schema.dump(transaction_type_data)

            logger.info("Response for put with id request for transaction type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Transaction type with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Transaction type with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def delete(self, transaction_type_id):
        """
             This is DELETE API
             Call this api passing a transaction type id
             parameters:
                 transaction_type: String
             responses:
                 404:
                     description: Transaction type with this id does not exist
                 200:
                     description: Transaction type with this id deleted successfully
                     schema:
                         TransactionTypeSchema
         """
        try:
            transaction_type_data = TransactionType.query.filter(TransactionType.id == transaction_type_id).first()
            db.session.delete(transaction_type_data)
            db.session.commit()

            logger.info("Response for delete request for transaction type:"
                        "Transaction type with this id deleted successfully")

            return "Transaction type record deleted successfully"
        except Exception:
            logger.exception("Response for delete request for transaction type:"
                             "Transaction type with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Transaction type with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class FundTransferResource(Resource):
    def post(self):
        """
             This is POST API
             parameters:
                 source: String
                 destination: String
             responses:
                 404:
                     description: Fund transfer does not exist
                 200:
                     description: Fund transfer record inserted successfully
                     schema:
                         FundTransferSchema
         """
        try:
            data = request.get_json()
            errors = fund_transfer_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data to create an activity")
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            fund_transfer_data = FundTransfer(
                source=data['source'],
                destination=data['destination'])

            db.session.add(fund_transfer_data)
            db.session.commit()
            result = fund_transfer_schema.dump(fund_transfer_data)
            logger.info("Response for post request for fund transfer {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Fund transfer record inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Fund transfer does not exist")
            response = ResponseGenerator(data={},
                                         message="Fund transfer does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def get(self):
        """
             This is GET API
             parameters:
                 source: String
                 destination: String
             responses:
                 404:
                     description: Fund transfer does not exist
                 200:
                     description: Fund transfer list return successfully
                     schema:
                         FundTransferSchema
         """
        try:
            fund_transfer_data = FundTransfer.query.all()
            if not fund_transfer_data:
                raise NoResultFound

            result = funds_transfer_schema.dump(fund_transfer_data)

            logger.info("Response for get request for fund transfer list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Fund transfer list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Fund transfer does not exist")
            response = ResponseGenerator(data={},
                                         message="Fund transfer does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class FundTransferResourceId(Resource):
    def get(self, fund_transfer_id):
        """
             This is GET API
             call this api passing fund transfer id
             parameters:
                 source: String
                 destination: String
             responses:
                 404:
                     description: Fund transfer with this id does not exist
                 200:
                     description: Fund transfer with this id return successfully
                     schema:
                         FundTransferSchema
         """
        try:
            fund_transfer_data = FundTransfer.query.filter(FundTransfer.id == fund_transfer_id).first()
            if not fund_transfer_data:
                raise NoResultFound

            result = fund_transfer_schema.dump(fund_transfer_data)

            logger.info("Response for get with id request for fund transfer list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Fund transfer with this  id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Fund transfer with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Fund transfer with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def put(self, fund_transfer_id):
        """
             This is PUT API
             Call this api passing a fund transfer id
             parameters:
                 source: String
                 destination: String
             responses:
                 404:
                     description: Fund transfer with this id does not exist
                 200:
                     description: Fund transfer with this id updated successfully
                     schema:
                         FundTransferSchema
         """
        try:
            # retrieve body data from input JSON
            data = request.get_json()
            errors = fund_transfer_schema.validate(data, partial=True)
            if errors:
                logger.error("Missing or sending incorrect data to create an activity {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            fund_transfer_data = FundTransfer.query.filter(FundTransfer.id == fund_transfer_id).first()
            if not fund_transfer_data:
                raise NoResultFound

            fund_transfer_data.source = data.get('source', fund_transfer_data.source)
            fund_transfer_data.destination = data.get('destination', fund_transfer_data.destination)

            db.session.commit()
            result = fund_transfer_schema.dump(fund_transfer_data)

            logger.info("Response for put with id request for fund transfer {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Fund transfer with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except NoResultFound:
            logger.exception("Fund transfer with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Fund transfer with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

    def delete(self, fund_transfer_id):
        """
             This is DELETE API
             Call this api passing a fund transfer id
             parameters:
                 source: String
                 destination: String
             responses:
                 404:
                     description: Fund transfer with this id does not exist
                 200:
                     description: Fund transfer with this id deleted successfully
                     schema:
                         FundTransferSchema
         """
        try:
            fund_transfer_data = FundTransfer.query.filter(FundTransfer.id == fund_transfer_id).first()
            db.session.delete(fund_transfer_data)
            db.session.commit()

            logger.info("Response for delete request for fund transfer:"
                        "Fund transfer with this id deleted successfully")

            return "Fund transfer record deleted successfully"
        except Exception:
            logger.exception("Response for delete request for fund transfer:"
                             "Fund transfer with this id does not exist")
            response = ResponseGenerator(data={},
                                         message="Fund transfer with this id does not exist",
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()
