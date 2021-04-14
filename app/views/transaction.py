from app import db
from app.common.custom_exception import BankAccountObjectNotFound, TransactionTypeObjectNotFound, AccountTransactionDetailsObjectNotFound, FundTransferObjectNotFound, MiniStatementObjectNotFound
from app.common.log import logger
from flask import request
from flask_restplus import Resource
from app.models.account import BankAccount
from app.models.transaction import AccountTransactionDetails, TransactionType, FundTransfer
from app.schemas.transaction import account_transaction_details_schema, accounts_transaction_details_schema, transaction_type_schema, transactions_type_schema, fund_transfer_schema, funds_transfer_schema
from app.common.response_genarator import ResponseGenerator
from http import HTTPStatus
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc


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

        data = request.get_json()
        errors = account_transaction_details_schema.validate(data, partial=True)
        if errors:
            logger.error("Missing or sending incorrect data to create an activity {}".format(errors))
            response = ResponseGenerator(data={},
                                         message=errors,
                                         success=False,
                                         status=HTTPStatus.BAD_REQUEST)
            return response.error_response()

        try:
            # get bank account details
            bank_account = BankAccount.query.filter(BankAccount.id == data['bank_account_id']).first()
            if not bank_account:
                raise BankAccountObjectNotFound("Invalid Bank Account")

            # get transaction type details
            transactions_type = TransactionType.query.filter(TransactionType.id == data['transaction_type_id']).first()
            if not transactions_type:
                raise TransactionTypeObjectNotFound("Invalid Transaction Type")

            # for credit
            if transactions_type.transaction_type.lower() == 'credit':
                bank_account.account_balance += data['transaction_amount']
                db.session.add(bank_account)
                transaction_status = "success"
            # for debit
            elif transactions_type.transaction_type.lower() == 'debit':
                if bank_account.account_balance - 1000 - data['transaction_amount'] > 0:
                    bank_account.account_balance -= data['transaction_amount']
                    db.session.add(bank_account)
                    transaction_status = "success"
                else:
                    transaction_status = "failed"

            # fund transfer type - funds withdraw
            fund_transfer_data = FundTransfer(
                from_account=bank_account.account_number,
                to_account=None
            )

            db.session.add(fund_transfer_data)
            db.session.commit()
            fund_transfer = fund_transfer_schema.dump(fund_transfer_data)

            # create account transaction
            bank_account_data = AccountTransactionDetails(
                transaction_amount=data['transaction_amount'],
                transaction_status=transaction_status,
                bank_account_id=data['bank_account_id'],
                transaction_type_id=data['transaction_type_id'],
                fund_transfer_id=fund_transfer.get('id'),
                fund_transfer_info=data['fund_transfer_info']
            )

            db.session.add(bank_account_data)
            db.session.commit()
            result = account_transaction_details_schema.dump(bank_account_data)
            logger.info("Response for get request for account transaction details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details added successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()

        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except TransactionTypeObjectNotFound as err:
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
                raise AccountTransactionDetailsObjectNotFound("Account transaction details does not exist")

            result = accounts_transaction_details_schema.dump(account_transaction_details_data)

            logger.info("Response for get request for account transaction details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except AccountTransactionDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
                raise AccountTransactionDetailsObjectNotFound("Account transaction details does not exist")

            result = account_transaction_details_schema.dump(account_transaction_details_data)

            logger.info("Response for get request for account transaction details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except AccountTransactionDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
                raise AccountTransactionDetailsObjectNotFound("Account transaction details with this id does not exist")

            account_transaction_details_data.transaction_amount = data.get('transaction_amount', account_transaction_details_data.transaction_amount)
            account_transaction_details_data.bank_account_id = data.get('bank_account_id', account_transaction_details_data.bank_account_id)
            account_transaction_details_data.transaction_type_id = data.get('transaction_type_id', account_transaction_details_data.transaction_type_id)
            account_transaction_details_data.fund_transfer_id = data.get('fund_transfer_id', account_transaction_details_data.fund_transfer_id)
            account_transaction_details_data.fund_transfer_type = data.get('fund_transfer_type', account_transaction_details_data.fund_transfer_type)

            db.session.commit()
            result = account_transaction_details_schema.dump(account_transaction_details_data)

            logger.info("Response for put with id request for account transaction details {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()

        except AccountTransactionDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
            if not account_transaction_details_data:
                raise AccountTransactionDetailsObjectNotFound("Account transaction details with this id does not exist")

            db.session.delete(account_transaction_details_data)
            db.session.commit()

            logger.info("Response for delete request for account transaction details:"
                        "Account transaction details with this id deleted successfully")

            return "Account transaction details record deleted successfully"
        except AccountTransactionDetailsObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
                raise TransactionTypeObjectNotFound("Transaction type does not exist")

            result = transactions_type_schema.dump(transaction_type_data)
            logger.info("Response for get request for transaction type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except TransactionTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
                raise TransactionTypeObjectNotFound("Transaction type with this id does not exist")

            result = transaction_type_schema.dump(transaction_type_data)

            logger.info("Response for get with id request for transaction type list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type with this  id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except TransactionTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
                raise TransactionTypeObjectNotFound("Transaction type with this id does not exist")

            transaction_type_data.transaction_type = data.get('transaction_type', transaction_type_data.transaction_type)
            db.session.commit()
            result = transaction_type_schema.dump(transaction_type_data)

            logger.info("Response for put with id request for transaction type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except TransactionTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
            if not transaction_type_data:
                raise TransactionTypeObjectNotFound("Transaction type with this id does not exist")

            db.session.delete(transaction_type_data)
            db.session.commit()

            logger.info("Response for delete request for transaction type:"
                        "Transaction type with this id deleted successfully")

            return "Transaction type record deleted successfully"
        except TransactionTypeObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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

            # fund transfer type - funds transfer
            fund_transfer_data = FundTransfer(
                from_account=data['from_account'],
                to_account=data['to_account'])

            db.session.add(fund_transfer_data)
            db.session.commit()
            result = fund_transfer_schema.dump(fund_transfer_data)

            from_bank_account = BankAccount.query.filter(BankAccount.account_number == data['from_account']).first()
            if not from_bank_account:
                raise BankAccountObjectNotFound("Bank account details does not exist")

            to_bank_account = BankAccount.query.filter(BankAccount.account_number == data['to_account']).first()
            if not to_bank_account:
                raise BankAccountObjectNotFound("Bank account details does not exist")

            transaction_type = TransactionType.query.filter(TransactionType.transaction_type == "debit").first()
            if not transaction_type:
                raise TransactionTypeObjectNotFound("Transaction type does not exist")

            if from_bank_account.account_balance - 1000 - data['transaction_amount'] > 0:
                from_bank_account.account_balance -= data['transaction_amount']
                db.session.add(from_bank_account)
                to_bank_account.account_balance += data['transaction_amount']
                db.session.add(to_bank_account)
                transaction_status = "success"
            else:
                transaction_status = "failed"

            account_transaction_data = AccountTransactionDetails(
                transaction_amount=data['transaction_amount'],
                transaction_status=transaction_status,
                bank_account_id=from_bank_account.id,
                transaction_type_id=transaction_type.id,
                fund_transfer_id=result.get('id'),
                fund_transfer_info="Funds Transfer"
            )

            db.session.add(account_transaction_data)
            db.session.commit()
            account_transaction_details_schema.dump(account_transaction_data)

            logger.info("Response for post request for fund transfer {}".format(result))
            if transaction_status == 'success':
                response = ResponseGenerator(data=result,
                                             message="Fund transfer successfully",
                                             success=True,
                                             status=HTTPStatus.OK)
            else:
                response = ResponseGenerator(data=result,
                                             message="Fund transfer declined",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
            return response.success_response()

        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()

        except TransactionTypeObjectNotFound as err:
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
                raise FundTransferObjectNotFound("Fund transfer does not exist")

            result = funds_transfer_schema.dump(fund_transfer_data)
            logger.info("Response for get request for fund transfer list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Fund transfer list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except FundTransferObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
                raise FundTransferObjectNotFound("Fund transfer with this id does not exist")

            result = fund_transfer_schema.dump(fund_transfer_data)

            logger.info("Response for get with id request for fund transfer list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Fund transfer with this  id return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except FundTransferObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
                raise FundTransferObjectNotFound("Fund transfer with this id does not exist")

            fund_transfer_data.from_account = data.get('from_account', fund_transfer_data.from_account)
            fund_transfer_data.to_account = data.get('to_account', fund_transfer_data.to_account)

            db.session.commit()
            result = fund_transfer_schema.dump(fund_transfer_data)

            logger.info("Response for put with id request for fund transfer {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Fund transfer with this id updated successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except FundTransferObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
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
            if not fund_transfer_data:
                raise FundTransferObjectNotFound("Fund transfer with this id does not exist")

            db.session.delete(fund_transfer_data)
            db.session.commit()

            logger.info("Response for delete request for fund transfer:"
                        "Fund transfer with this id deleted successfully")

            return "Fund transfer record deleted successfully"
        except FundTransferObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()


class MiniStatementResources(Resource):
    def get(self):
        try:
            mini_statement_data = AccountTransactionDetails.query.order_by(desc(AccountTransactionDetails.id)).limit(10)
            if not mini_statement_data:
                raise MiniStatementObjectNotFound("Account transaction details records does not exist")

            result = accounts_transaction_details_schema.dump(mini_statement_data)
            logger.info("Response for get request for account transaction details list of records {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details list of records return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except MiniStatementObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
            return response.error_response()
