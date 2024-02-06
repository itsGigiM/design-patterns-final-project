from typing import Protocol

from core.constants import (
    MINIMUM_TRANSACTION_FEE,
    SAME_OWNERS_TRANSACTION_FEE,
    SATOSHIS_IN_ONE_BITCOIN,
    TRANSACTION_FEE,
)


class IFeeStrategy(Protocol):
    def calculate_transaction_fee(
        self, amount: float, from_wallet_owner: str, to_wallet_owner: str
    ) -> float:
        pass


class FeeStrategy(IFeeStrategy):
    def calculate_transaction_fee(
        self, amount: float, from_wallet_owner: str, to_wallet_owner: str
    ) -> float:
        if from_wallet_owner == to_wallet_owner:
            return SAME_OWNERS_TRANSACTION_FEE

        amount_satoshis = amount * SATOSHIS_IN_ONE_BITCOIN
        transaction_fee = max(
            MINIMUM_TRANSACTION_FEE, amount_satoshis * TRANSACTION_FEE
        )
        return transaction_fee / SATOSHIS_IN_ONE_BITCOIN
