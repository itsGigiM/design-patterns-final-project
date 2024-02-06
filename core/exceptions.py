from typing import Protocol

from fastapi import HTTPException, status


class ICustomExceptionFactory(Protocol):
    @staticmethod
    def custom_exception() -> HTTPException:
        pass


class APINotValidError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"message": "API is not valid"}},
        )


class UserExistsError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "User already exists"}},
        )


class CanNotConnectToDatabaseError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot connect to database"}},
        )


class MailNotValidError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": {"message": "Given mail is no valid"}},
        )


class CanNotUpdateWalletNumberError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot update wallet number"}},
        )


class CanNotUpdateWalletBalanceError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot update wallet balance"}},
        )


class CanNotGetWalletBalanceError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot get wallet balance"}},
        )


class WalletDoesNotExistError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Wallet does not exist"}},
        )


class UserDoesNotExistError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Given user does not exist"}},
        )


class CanNotGetUserError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Could not get user"}},
        )


class CanNotGetTransactionsError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot get transaction"}},
        )


class CanNotGetStatisticsError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot get statistics"}},
        )


class CanNotCreateWalletError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot create wallet"}},
        )


class TooManyWalletsError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Wallet number exceeds 3"}},
        )


class UnsuitableAPIKeyError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": {"message": "Api key is not suitable"}},
        )


class IntoSameWalletTransactionError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Cannot transfer to the same wallet"}},
        )


class NotEnoughBalanceError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Not enough balance"}},
        )


class NoAdminPrivilegesError(ICustomExceptionFactory):
    @staticmethod
    def custom_exception() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": {"message": "Check admin api key"}},
        )
