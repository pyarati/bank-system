# define Python user-defined exceptions
class ExceptionHandler(Exception):
    """Base class for other exceptions"""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


class UserObjectNotFound(ExceptionHandler):
    """Raised when User Object Not Found"""
    pass


class UserTypeObjectNotFound(ExceptionHandler):
    """Raised when User Type Object Not Found"""
    pass


class BankAccountObjectNotFound(ExceptionHandler):
    """Raised when Bank Account Object Not Found"""
    pass


class AccountTypeObjectNotFound(ExceptionHandler):
    """Raised when Account Type Object Not Found"""
    pass


class BranchDetailsObjectNotFound(ExceptionHandler):
    """Raised when Branch Details Object Not Found"""
    pass


class AccountTransactionDetailsObjectNotFound(ExceptionHandler):
    """Raised when Account Transaction Details Object Not Found"""
    pass


class TransactionTypeObjectNotFound(ExceptionHandler):
    """Raised when Transaction Type Object Not Found"""
    pass


class FundTransferObjectNotFound(ExceptionHandler):
    """Raised when Fund Transfer Object Not Found"""
    pass


class MiniStatementObjectNotFound(ExceptionHandler):
    """Raised when Mini Statement Object Not Found"""
    pass
