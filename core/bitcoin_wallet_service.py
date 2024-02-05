from typing import Any
from uuid import UUID

from core.constants import DEFAULT_WALLET_PREFIX
from core.model.request.request import TransactionRequest
from core.model.response.response import StatisticsResponse, TransactionResponse
from core.service_interface.transaction_service_interface import ITransactionService
from core.service_interface.user_service_interface import IUserService
from core.service_interface.wallet_service_interface import IWalletService
from core.transaction import Transaction
from core.wallet import WalletUSD


class BitcoinWalletService:
    def __init__(self,
                 user_service: IUserService,
                 wallet_service: IWalletService,
                 transaction_service: ITransactionService):
        self.user_service = user_service
        self.wallet_service = wallet_service
        self.transaction_service = transaction_service

    def register_user(self, user_data: str) -> UUID:
        res = self.user_service.register_user(user_data)
        self.wallet_service.create_default_wallet(DEFAULT_WALLET_PREFIX + str(res), str(res))
        return res

    def validate_api_key(self, api_key: str) -> bool:
        res = self.wallet_service.get_wallet(DEFAULT_WALLET_PREFIX + str(api_key))
        if res is None:
            raise Exception("Api key is not valid")
        return True

    def create_wallet(self, api_key: str) -> WalletUSD:
        if self.validate_api_key(api_key):
            return self.wallet_service.create_wallet(api_key)

    def get_wallet(self, address: str, api_key: str) -> WalletUSD:
        if self.validate_api_key(api_key):
            return self.wallet_service.get_wallet(address)

    def make_transaction(self, r: TransactionRequest, api_key) -> None:
        if self.validate_api_key(api_key):
            self.transaction_service.create_transaction(r.from_wallet, r.to_wallet, r.amount_btc)

    def get_transactions(self, api_key: str) -> list[Any]:
        if self.validate_api_key(api_key):
            return self.transaction_service.get_transactions(api_key)

    def get_wallet_transactions(self, address: str, api_key: str) -> list[Any]:
        if self.validate_api_key(api_key):
            return self.transaction_service.get_wallet_transactions(api_key, address)

    def get_statistics(self) -> StatisticsResponse:
        res = self.transaction_service.get_statistics()
        return StatisticsResponse(res["amount"], res["sum"])
