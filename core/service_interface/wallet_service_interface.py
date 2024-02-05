import uuid
from typing import Protocol

from core.constants import BTC_STARTING_BALANCE, DEFAULT_WALLET_BALANCE
from core.repository_interface.wallet_repository_interface import IWalletRepository
from core.wallet import WalletUSD
from core.walletToWalletUSDAdapter import IWalletToWalletUSDAdapter


class IWalletService(Protocol):
    def create_wallet(self, api_key: str) -> WalletUSD:
        pass

    def create_default_wallet(self, address: str, api_key: str) -> None:
        pass

    def get_wallet(self, address: str) -> WalletUSD:
        pass


class WalletService(IWalletService):
    wallet_rep: IWalletRepository

    def __init__(
        self, wallet_repository: IWalletRepository, adapter: IWalletToWalletUSDAdapter
    ):
        self.wallet_rep = wallet_repository
        self.adapter = adapter

    def create_wallet(self, api_key: str) -> WalletUSD:
        address = uuid.uuid4()
        start_b = BTC_STARTING_BALANCE
        if self.wallet_rep.create_wallet(api_key, str(address), start_b):
            wallet = self.wallet_rep.get_wallet(address=str(address))
            return self.adapter.convert(wallet)

    def create_default_wallet(self, address: str, api_key: str) -> None:
        self.wallet_rep.create_wallet(api_key, address, DEFAULT_WALLET_BALANCE)

    def get_wallet(self, address: str) -> WalletUSD:
        wallet = self.wallet_rep.get_wallet(address=address)
        return self.adapter.convert(wallet)
