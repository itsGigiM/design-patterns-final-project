from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from core.constants import SATOSHIS_IN_ONE_BITCOIN, TRANSACTION_FEE


@dataclass
class Transaction(Protocol):
    from_wallet_address: UUID
    to_wallet_address: UUID
    amount: float
    transaction_id: UUID

    def calculate_transaction_fee(self, wallets_database: WalletsRepository) -> float:
        pass


@dataclass
class StandardTransaction(Protocol):
    from_wallet_address: UUID
    to_wallet_address: UUID
    amount: float
    transaction_id: UUID = field(default_factory=uuid4)

    def calculate_transaction_fee(self, wallets_database: WalletsRepository) -> float:
        from_owner = wallets_database.get_owner_id(self.from_wallet_address)
        to_owner = wallets_database.get_owner_id(self.to_wallet_address)
        if from_owner == to_owner:
            return 0

        amount_satoshis = self.amount * SATOSHIS_IN_ONE_BITCOIN
        transaction_fee = max(1, amount_satoshis * TRANSACTION_FEE)
        return transaction_fee / SATOSHIS_IN_ONE_BITCOIN
