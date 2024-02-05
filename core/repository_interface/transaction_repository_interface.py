from typing import Any, Protocol


class ITransactionRepository(Protocol):
    def create_transaction(
        self, from_wallet: str, to_wallet: str, sent_amount: float, fee_amount: float
    ) -> bool:
        pass

    def get_all_transactions(self) -> Any:
        pass

    def get_wallet_all_transactions(self, wallet: str) -> Any:
        pass

    def get_statistics(self) -> dict[str, Any]:
        pass
