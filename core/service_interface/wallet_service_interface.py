import uuid
from asyncio import Protocol

from core.WalletToWalletUSDAdapter import IWalletToWalletUSDAdapter
from core.constants import BTC_STARTING_BALANCE
from core.repository_interface.wallet_repository_interface import IWalletRepository
from core.wallet import WalletUSD


class IWalletService(Protocol):
    def create_wallet(self, api_key: str) -> WalletUSD:
        pass

    def get_wallet(self, address: str) -> WalletUSD:
        pass


class WalletService(IWalletService):
    wallet_rep: IWalletRepository

    def __init__(self, wallet_repository: IWalletRepository, adapter: IWalletToWalletUSDAdapter):
        self.wallet_rep = wallet_repository
        self.adapter = adapter

    def create_wallet(self, api_key: str) -> WalletUSD:
        address = uuid.uuid4()
        starting_balance = BTC_STARTING_BALANCE
        self.wallet_rep.create_wallet(api_key, address, starting_balance)
        return WalletUSD(usd_amount=1, address=address, btc_amount=starting_balance)

    def get_wallet(self, address: str) -> WalletUSD:
        wallet = self.wallet_rep.get_wallet(address=address)
        return self.adapter.convert(wallet)
