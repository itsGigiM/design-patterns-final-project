from dataclasses import dataclass

from pydantic import BaseModel

from core.transaction import Transaction


@dataclass
class UserRegistrationResponse(BaseModel):
    api_key: str


@dataclass
class WalletResponse(BaseModel):
    wallet_address: str
    balance_btc: float
    balance_usd: float


@dataclass
class TransactionResponse(BaseModel):
    transactions: list[Transaction]


@dataclass
class StatisticsResponse(BaseModel):
    transaction_amount: int
    transaction_sum: float
