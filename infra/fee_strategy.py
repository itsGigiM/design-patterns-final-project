from typing import Protocol

from core.constants import SATOSHIS_IN_ONE_BITCOIN, TRANSACTION_FEE


class IFeeStrategy(Protocol):
    @staticmethod
    def calculate_transaction_fee(
            amount: float, from_wallet_owner: str, to_wallet_owner: str
    ) -> float:
        pass


class FeeStrategy(IFeeStrategy):
    @staticmethod
    def calculate_transaction_fee(
            amount: float, from_wallet_owner: str, to_wallet_owner: str
    ) -> float:
        if from_wallet_owner == to_wallet_owner:
            return 0

        amount_satoshis = amount * SATOSHIS_IN_ONE_BITCOIN
        transaction_fee = max(1, amount_satoshis * TRANSACTION_FEE)
        return transaction_fee / SATOSHIS_IN_ONE_BITCOIN
