from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from core.BTCtoUSDconverter import IBTCtoUSDConverter


@dataclass
class IWallet(Protocol):
    address: UUID
    api_key: UUID
    # def get_address(self) -> UUID:
    #     pass
    #
    # def get_balance_in_btc(self) -> float:
    #     pass
    #
    # def get_balance_in_usd(self) -> float:
    #     pass
    #
    # def get_balance(self) -> dict[str, str]:
    #     pass


@dataclass
class Wallet(IWallet):
    address: UUID
    api_key: UUID
    # in BTC
    amount: float

    def __hash__(self) -> int:
        return hash(self.address)
    #
    # def get_address(self) -> UUID:
    #     return self.address
    #
    # def get_balance_in_btc(self) -> float:
    #     return self.amount
    #
    # def get_balance_in_usd(self) -> float:
    #     return self.converter.convert(self.amount)
    #
    # def get_balance(self) -> dict[str, str]:
    #     balance_in_usd = self.get_balance_in_usd()
    #     return {
    #         "address": str(self.address),
    #         "balance_btc": str(self.amount),
    #         "balance_usd": str(balance_in_usd),
    #     }


@dataclass
class WalletUSD(Wallet):
    usd_amount: float
    api_key: UUID
    address: UUID
    btc_amount: float
