from typing import Protocol

from core.constants import SATOSHIS_IN_ONE_BITCOIN, TRANSACTION_FEE
from core.repository_interface.wallet_repository_interface import IWalletRepository


class IFeeStrategy(Protocol):
    @staticmethod
    def calculate_transaction_fee(
        amount: float,
        from_wallet: str,
        to_wallet: str,
        wallets_database: IWalletRepository,
    ) -> float:
        pass


class FeeStrategy(Protocol):
    @staticmethod
    def calculate_transaction_fee(
        amount: float,
        from_wallet: str,
        to_wallet: str,
        wallets_database: IWalletRepository,
    ) -> float:
        from_owner = wallets_database.get_user(from_wallet)
        to_owner = wallets_database.get_user(to_wallet)
        if from_owner == to_owner:
            return 0

        amount_satoshis = amount * SATOSHIS_IN_ONE_BITCOIN
        transaction_fee = max(1, amount_satoshis * TRANSACTION_FEE)
        return transaction_fee / SATOSHIS_IN_ONE_BITCOIN
