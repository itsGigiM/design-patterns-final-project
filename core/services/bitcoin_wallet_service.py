from typing import Any
from uuid import UUID

from fastapi import HTTPException

from core.constants import ADMIN_API_KEY, DEFAULT_WALLET_PREFIX
from core.exceptions import (
    APINotValidError,
    NoAdminPrivilegesError,
    UnsuitableAPIKeyError, WalletDoesNotExistError,
)
from core.model.request.request import TransactionRequest
from core.model.response.response import StatisticsResponse
from core.services.transaction_service import ITransactionService
from core.services.user_service import IUserService
from core.services.wallet_service import IWalletService
from core.wallet import WalletUSD


class BitcoinWalletService:
    def __init__(
            self,
            user_service: IUserService,
            wallet_service: IWalletService,
            transaction_service: ITransactionService,
    ):
        self.user_service = user_service
        self.wallet_service = wallet_service
        self.transaction_service = transaction_service

    def register_user(self, user_data: str) -> UUID:
        res = self.user_service.register_user(user_data)
        self.wallet_service.create_default_wallet(
            DEFAULT_WALLET_PREFIX + str(res), str(res)
        )
        return res

    def validate_api_key(self, api_key: str) -> bool:
        try:
            res = self.wallet_service.get_wallet(DEFAULT_WALLET_PREFIX + str(api_key))
            if res is None:
                raise False
            return True
        except HTTPException:
            return False

    def create_wallet(self, api_key: str) -> WalletUSD:
        if self.validate_api_key(api_key):
            return self.wallet_service.create_wallet(api_key)
        raise APINotValidError.custom_exception()

    def get_wallet(self, address: str, api_key: str) -> WalletUSD:
        if self.validate_api_key(api_key):
            wallet = self.wallet_service.get_wallet(address)
            if str(wallet.api_key) != api_key:
                raise UnsuitableAPIKeyError.custom_exception()
            return wallet
        raise APINotValidError.custom_exception()

    def make_transaction(self, r: TransactionRequest, api_key: str) -> None:
        if self.validate_api_key(api_key):
            from_wal = self.get_wallet(r.from_wallet, api_key)
            if str(from_wal.api_key) != api_key:
                raise UnsuitableAPIKeyError.custom_exception()
            self.transaction_service.create_transaction(
                r.from_wallet, r.to_wallet, r.amount_btc
            )
        raise APINotValidError.custom_exception()

    def get_transactions(self, api_key: str) -> list[Any]:
        if self.validate_api_key(api_key):
            return self.transaction_service.get_transactions(api_key)
        raise APINotValidError.custom_exception()

    def get_wallet_transactions(self, address: str, api_key: str) -> list[Any]:
        if self.validate_api_key(api_key):
            wal = self.get_wallet(address, api_key)
            if str(wal.api_key) != api_key:
                raise UnsuitableAPIKeyError.custom_exception()
            return self.transaction_service.get_wallet_transactions(api_key, address)
        raise APINotValidError.custom_exception()

    def get_statistics(self, api_key: str) -> StatisticsResponse:
        if api_key != ADMIN_API_KEY:
            raise NoAdminPrivilegesError.custom_exception()
        res = self.transaction_service.get_statistics()
        return StatisticsResponse(res["amount"], res["sum"])
