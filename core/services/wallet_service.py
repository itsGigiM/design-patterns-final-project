import uuid
from typing import Protocol

from core.constants import BTC_STARTING_BALANCE, DEFAULT_WALLET_BALANCE, MAX_WALLETS
from core.exceptions import CanNotCreateWalletError, TooManyWalletsError
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

    def __init__(
        self, wallet_repository: IWalletRepository, adapter: IWalletToWalletUSDAdapter
    ):
        self.wallet_rep = wallet_repository
        self.adapter = adapter

    def create_wallet(self, api_key: str) -> WalletUSD:
        if len(self.wallet_rep.get_wallets(api_key)) - 1 >= MAX_WALLETS:
            raise TooManyWalletsError.custom_exception()
        address = uuid.uuid4()
        start_b = BTC_STARTING_BALANCE
        if self.wallet_rep.create_wallet(api_key, str(address), start_b):
            wallet = self.wallet_rep.get_wallet(address=str(address))
            return self.adapter.convert(wallet)
        raise CanNotCreateWalletError.custom_exception()

    def create_default_wallet(self, address: str, api_key: str) -> None:
        self.wallet_rep.create_wallet(api_key, address, DEFAULT_WALLET_BALANCE)

    def get_wallet(self, address: str) -> WalletUSD:
        wallet = self.wallet_rep.get_wallet(address=address)
        return self.adapter.convert(wallet)
