from asyncio import Protocol

from core.wallet import WalletUSD


class IWalletService(Protocol):
    def create_wallet(self, api_key: str) -> WalletUSD:
        pass

    def get_wallet(self, address: str) -> WalletUSD:
        pass
