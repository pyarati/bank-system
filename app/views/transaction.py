from http import HTTPStatus
from flask import request
from flask_restplus import Resource
from sqlalchemy import desc
from app import db
from app.common.custom_exception import BankAccountObjectNotFound, TransactionTypeObjectNotFound, \
    AccountTransactionDetailsObjectNotFound, FundTransferObjectNotFound, MiniStatementObjectNotFound
from app.common.log import logger
from app.common.response_genarator import ResponseGenerator
from app.models.account import BankAccount
from app.models.transaction import AccountTransactionDetails, TransactionType, FundTransfer
from app.schemas.transaction import account_transaction_details_schema, accounts_transaction_details_schema, \
    transaction_type_schema, transactions_type_schema, fund_transfer_schema, funds_transfer_schema


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
            logger.error("Missing or sending incorrect data {}".format(errors))
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
                    raise FundTransferObjectNotFound("Transaction failed")

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
        except FundTransferObjectNotFound as err:
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
            account_transaction_details_data = AccountTransactionDetails.query.order_by(
                AccountTransactionDetails.bank_account_id)
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)

        return response.error_response()


class AccountTransactionDetailsResourceBankId(Resource):
    def get(self):
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
            bank_account_id = request.args.get("bank_account_id")
            if not bank_account_id:
                raise BankAccountObjectNotFound("Please provide valid bank account id")

            bank_account_data = AccountTransactionDetails.query.filter(
                AccountTransactionDetails.bank_account_id == bank_account_id).all()
            if not bank_account_data:
                raise AccountTransactionDetailsObjectNotFound("Transaction with this bank account not found")

            result = accounts_transaction_details_schema.dump(bank_account_data)

            logger.info("Response for get request for account transaction details list {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Account transaction details list return successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except BankAccountObjectNotFound as err:
            logger.exception(err.message)
            response = ResponseGenerator(data={},
                                         message=err.message,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)
        except AccountTransactionDetailsObjectNotFound as err:
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
                                         status=HTTPStatus.NOT_FOUND)

        return response.error_response()


class AccountTransactionDetailsResourceId(Resource):
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
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            account_transaction_details_data = AccountTransactionDetails.query.filter(
                AccountTransactionDetails.id == account_transaction_details_id).first()
            if not account_transaction_details_data:
                raise AccountTransactionDetailsObjectNotFound("Account transaction details with this id does not exist")

            account_transaction_details_data.transaction_amount = data.get('transaction_amount',
                                                                           account_transaction_details_data.transaction_amount)
            account_transaction_details_data.bank_account_id = data.get('bank_account_id',
                                                                        account_transaction_details_data.bank_account_id)
            account_transaction_details_data.transaction_type_id = data.get('transaction_type_id',
                                                                            account_transaction_details_data.transaction_type_id)
            account_transaction_details_data.fund_transfer_id = data.get('fund_transfer_id',
                                                                         account_transaction_details_data.fund_transfer_id)
            account_transaction_details_data.fund_transfer_type = data.get('fund_transfer_type',
                                                                           account_transaction_details_data.fund_transfer_type)

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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            transaction_type_data = TransactionType(
                transaction_type=data['transaction_type'])

            if transaction_type_data.transaction_type.lower() not in ["credit", "debit"]:
                raise TransactionTypeObjectNotFound("Transaction type does not exist")

            db.session.add(transaction_type_data)
            db.session.commit()
            result = transaction_type_schema.dump(transaction_type_data)
            logger.info("Response for post request for transaction type {}".format(result))
            response = ResponseGenerator(data=result,
                                         message="Transaction type list inserted successfully",
                                         success=True,
                                         status=HTTPStatus.OK)
            return response.success_response()
        except TransactionTypeObjectNotFound as err:
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
                logger.error("Missing or sending incorrect data {}".format(errors))
                response = ResponseGenerator(data={},
                                             message=errors,
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
                return response.error_response()

            transaction_type_data = TransactionType.query.filter(TransactionType.id == transaction_type_id).first()
            if not transaction_type_data:
                raise TransactionTypeObjectNotFound("Transaction type with this id does not exist")

            transaction_type_data.transaction_type = data.get('transaction_type',
                                                              transaction_type_data.transaction_type)
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
                logger.error("Missing or sending incorrect data {}".format(errors))
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

            # add transaction 'from bank account' as transaction type 'debit'
            from_bank_account = BankAccount.query.filter(BankAccount.account_number == data['from_account']).first()
            if not from_bank_account:
                raise BankAccountObjectNotFound("From bank account details does not exist")

            transaction_type_debit = TransactionType.query.filter(TransactionType.transaction_type == "debit").first()
            if not transaction_type_debit:
                raise TransactionTypeObjectNotFound("Transaction type does not exist")

            # add transaction 'to bank account' as transaction type 'credit'
            to_bank_account = BankAccount.query.filter(BankAccount.account_number == data['to_account']).first()
            if not to_bank_account:
                raise BankAccountObjectNotFound("To bank account details does not exist")

            transaction_type_credit = TransactionType.query.filter(TransactionType.transaction_type == "credit").first()
            if not transaction_type_credit:
                raise TransactionTypeObjectNotFound("Transaction type does not exist")

            if from_bank_account.account_balance - 1000 - data['transaction_amount'] > 0:
                from_bank_account.account_balance -= data['transaction_amount']
                db.session.add(from_bank_account)
                to_bank_account.account_balance += data['transaction_amount']
                db.session.add(to_bank_account)
                transaction_status = "success"
            else:
                transaction_status = "failed"

            # create account transaction for from bank account
            account_transaction_data = AccountTransactionDetails(
                transaction_amount=data['transaction_amount'],
                transaction_status=transaction_status,
                bank_account_id=from_bank_account.id,
                transaction_type_id=transaction_type_debit.id,
                fund_transfer_id=result.get('id'),
                fund_transfer_info="Funds Transfer"
            )
            db.session.add(account_transaction_data)
            db.session.commit()
            account_transaction_details_schema.dump(account_transaction_data)

            # create account transaction for to bank account
            account_transaction_data = AccountTransactionDetails(
                transaction_amount=data['transaction_amount'],
                transaction_status=transaction_status,
                bank_account_id=to_bank_account.id,
                transaction_type_id=transaction_type_credit.id,
                fund_transfer_id=result.get('id'),
                fund_transfer_info="Funds Received"
            )
            db.session.add(account_transaction_data)
            db.session.commit()
            account_transaction_details_schema.dump(account_transaction_data)

            logger.info("Response for post request for fund transfer {}".format(result))
            if transaction_status == 'success':
                response = ResponseGenerator(data=result,
                                             message="Fund transferred successfully",
                                             success=True,
                                             status=HTTPStatus.OK)
            else:
                response = ResponseGenerator(data=result,
                                             message="Fund transfer declined, Please maintain minimum balance in account",
                                             success=False,
                                             status=HTTPStatus.BAD_REQUEST)
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
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
                logger.error("Missing or sending incorrect data {}".format(errors))
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)

        return response.error_response()


class MiniStatementResources(Resource):
    def get(self, bank_account_id):
        try:
            bank_account_data = BankAccount.query.filter(BankAccount.id == bank_account_id).first()
            if bank_account_data:
                mini_statement_data = AccountTransactionDetails.query.filter(
                    AccountTransactionDetails.bank_account_id == bank_account_id).order_by(
                    desc(AccountTransactionDetails.id)).limit(10)
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
        except Exception as err:
            logger.exception(err)
            response = ResponseGenerator(data={},
                                         message=err,
                                         success=False,
                                         status=HTTPStatus.NOT_FOUND)

        return response.error_response()
