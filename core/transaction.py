from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass
class ITransaction(Protocol):
    from_wallet_address: UUID
    to_wallet_address: UUID
    sent_amount: float
    fee_amount: float
    total_amount: float


@dataclass
class Transaction(ITransaction):
    from_wallet_address: UUID
    to_wallet_address: UUID
    sent_amount: float
    fee_amount: float
    total_amount: float
