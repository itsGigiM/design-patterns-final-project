from typing import Any, Optional, Protocol


class IWalletRepository(Protocol):
    def create_wallet(self, user: str, address: str, btc_balance: int = 1) -> bool:
        pass

    def exists_wallet(self, address: str) -> bool:
        pass

    def change_balance(self, address: str, balance_change: int) -> None:
        pass

    def get_balance(self, address: str) -> int:
        pass

    def get_wallet(self, address: str) -> Optional[Any]:
        pass

    def get_wallets(self, user: str) -> Any:
        pass
