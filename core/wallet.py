from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass
class IWallet(Protocol):
    address: UUID
    api_key: UUID
    amount: float


@dataclass
class Wallet(IWallet):
    address: UUID
    api_key: UUID
    # in BTC
    amount: float

    def __hash__(self) -> int:
        return hash(self.address)


@dataclass
class WalletUSD(Wallet):
    usd_amount: float
