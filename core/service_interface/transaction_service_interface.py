from asyncio import Protocol
from typing import Any

from core.repository_interface.transaction_repository_interface import ITransactionRepository
from core.repository_interface.wallet_repository_interface import IWalletRepository
from infra.fee_strategy import IFeeStrategy, FeeStrategy


class ITransactionService(Protocol):
    def create_transaction(self, from_wallet: str, to_wallet: str, amount_btc: float) -> None:
        pass

    def get_statistics(self) -> dict[str, Any]:
        pass


class TransactionService(ITransactionService):
    def __init__(self, transactions_repository: ITransactionRepository, fee_strategy: IFeeStrategy,
                 wallets_repository: IWalletRepository):
        self.transactions_repository = transactions_repository
        self.fee_strategy = fee_strategy
        self.wallets_repository = wallets_repository

    def create_transaction(self, from_wallet: str, to_wallet: str, amount_btc: float) -> None:
        transaction_fee = self.fee_strategy.calculate_transaction_fee(amount_btc, from_wallet, to_wallet,
                                                                      self.wallets_repository)
        sent_amount = amount_btc - transaction_fee
        self.transactions_repository.create_Transaction(from_wallet, to_wallet, sent_amount, transaction_fee)

    def get_statistics(self) -> dict[str, Any]:
        res = self.transactions_repository.get_statistics()
        return {"amount": res["transaction_total_number"],
                "sum": res["transaction_total_amount"]}
