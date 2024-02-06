from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class UserRegistrationRequest(BaseModel):
    email: str


@dataclass
class WalletCreationRequest(BaseModel):
    pass


@dataclass
class TransactionRequest(BaseModel):
    from_wallet: str
    to_wallet: str
    amount_btc: float
