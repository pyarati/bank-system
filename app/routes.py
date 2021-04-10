from app import api
from app.views.user import UserResources, UserResourcesId, UserTypeResource, UserTypeResourceId
from app.views.account import BankAccountResource, BankAccountResourceId, AccountTypeResource, AccountTypeResourceId, BranchDetailsResource, BranchDetailsResourceId
from app.views.transaction import AccountTransactionDetailsResource, AccountTransactionDetailsResourceId, TransactionTypeResource, TransactionTypeResourceId, FundTransferResource, FundTransferResourceId, MiniStatementResources


api.add_resource(UserResources, '/user')
api.add_resource(UserResourcesId, '/user/<int:user_id>')
api.add_resource(UserTypeResource, '/usertype')
api.add_resource(UserTypeResourceId, '/usertype/<int:user_type_id>')
api.add_resource(BankAccountResource, '/bankaccount')
api.add_resource(BankAccountResourceId, '/bankaccount/<int:bank_account_id>')
api.add_resource(AccountTypeResource, '/accounttype')
api.add_resource(AccountTypeResourceId, '/accounttype/<int:account_type_id>')
api.add_resource(BranchDetailsResource, '/branchdetails')
api.add_resource(BranchDetailsResourceId, '/branchdetails/<int:branch_details_id>')
api.add_resource(AccountTransactionDetailsResource, '/accounttransactiondetails')
api.add_resource(AccountTransactionDetailsResourceId, '/accounttransactiondetails/<int:account_transaction_details_id>')
api.add_resource(TransactionTypeResource, '/transactiontype')
api.add_resource(TransactionTypeResourceId, '/transactiontype/<int:transaction_type_id>')
api.add_resource(FundTransferResource, '/fundtransfer')
api.add_resource(FundTransferResourceId, '/fundtransfer/<int:fund_transfer_id>')
api.add_resource(MiniStatementResources, '/ministatement')
