from asyncio import Protocol
from typing import Any


class ITransactionService(Protocol):
    def create_transaction(self, from_wallet: str, to_wallet: str, amount_btc: float) -> None:
        pass

    def get_statistics(self) -> dict[str, Any]:
        pass
