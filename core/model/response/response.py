from dataclasses import dataclass
from typing import Any


@dataclass
class UserRegistrationResponse:
    api_key: str


@dataclass
class WalletResponse:
    wallet_address: str
    balance_btc: float
    balance_usd: float


@dataclass
class TransactionResponse:
    transactions: list[Any]


@dataclass
class StatisticsResponse:
    transaction_amount: int
    transaction_sum: float
