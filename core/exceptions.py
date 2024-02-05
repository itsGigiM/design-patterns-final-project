class APINotValidError(Exception):
    pass


class UserExistsError(Exception):
    pass


class CanNotConnectToDatabaseError(Exception):
    pass


class MailNotValidError(Exception):
    pass


class CanNotUpdateWalletNumberError(Exception):
    pass


class CanNotUpdateWalletBalanceError(Exception):
    pass


class CanNotGetWalletBalanceError(Exception):
    pass


class WalletDoesNotExistError(Exception):
    pass


class UserDoesNotExistError(Exception):
    pass


class CanNotGetUserError(Exception):
    pass


class CanNotGetTransactionsError(Exception):
    pass


class CanNotGetStatisticsError(Exception):
    pass
