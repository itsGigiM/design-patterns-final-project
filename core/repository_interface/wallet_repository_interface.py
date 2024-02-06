from typing import Protocol

from core.constants import BTC_STARTING_BALANCE
from core.wallet import Wallet


class IWalletRepository(Protocol):
    def create_wallet(
        self, api_key: str, address: str, btc_balance: float = BTC_STARTING_BALANCE
    ) -> bool:
        pass

    def exists_wallet(self, address: str) -> bool:
        pass

    def change_balance(self, address: str, balance_change: float) -> None:
        pass

    def get_balance(self, address: str) -> float:
        pass

    def get_user(self, address: str) -> str:
        pass

    def get_wallet(self, address: str) -> Wallet:
        pass

    def get_wallets(self, api_key: str) -> list[Wallet]:
        pass
