from typing import Any, Protocol

# transactions
# ------------
# fromWallet
# toWallet
# sentAmount
# feeAmount
# totalAmount(sum)


class ITransactionRepository(Protocol):
    def create_Transaction(
        self, from_wallet: str, to_wallet: str, sent_amount: float, fee_amount: float
    ) -> bool:
        pass

    def get_all_transactions(self) -> list[Any]:
        pass

    def get_wallet_all_transactions(self, wallet: str) -> Any:
        pass

    def get_statistics(self) -> dict[str, float]:
        pass
