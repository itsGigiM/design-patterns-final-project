from http.client import HTTPException
from uuid import UUID

from core.model.request.request import TransactionRequest
from core.model.response.response import StatisticsResponse, TransactionResponse
from core.service_interface.transaction_service_interface import ITransactionService
from core.service_interface.user_service_interface import IUserService
from core.service_interface.wallet_service_interface import IWalletService
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
        return self.user_service.register_user(user_data)

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        # TODO add retrieving wallets
        if api_key not in ["1"]:
            raise HTTPException(status_code=403, detail="Invalid API key")
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
            pass

    def get_transactions(self, api_key: str) -> TransactionResponse:
        pass
    
    def get_wallet_transactions(self, address: str, api_key: str) -> TransactionResponse:
        pass

    def get_statistics(self) -> StatisticsResponse:
        res = self.transaction_service.get_statistics()
        return StatisticsResponse(res["amount"], res["sum"])
