# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class UserObjectNotFound(Error):
    """Raised when User Object Not Found"""
    pass


class UserTypeObjectNotFound(Error):
    """Raised when User Type Object Not Found"""
    pass


class BankAccountObjectNotFound(Error):
    """Raised when Bank Account Object Not Found"""
    pass


class AccountTypeObjectNotFound(Error):
    """Raised when Account Type Object Not Found"""
    pass


class BranchDetailsObjectNotFound(Error):
    """Raised when Branch Details Object Not Found"""
    pass


class AccountTransactionDetailsObjectNotFound(Error):
    """Raised when Account Transaction Details Object Not Found"""
    pass


class TransactionTypeObjectNotFound(Error):
    """Raised when Transaction Type Object Not Found"""
    pass


class FundTransferObjectNotFound(Error):
    """Raised when Fund Transfer Object Not Found"""
    pass


class MiniStatementObjectNotFound(Error):
    """Raised when Mini Statement Object Not Found"""
    pass
