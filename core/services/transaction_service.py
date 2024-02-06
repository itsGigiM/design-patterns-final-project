from typing import Any, Protocol

from core.exceptions import IntoSameWalletTransactionError, NotEnoughBalanceError
from core.repository_interface.transaction_repository_interface import (
    ITransactionRepository,
)
from core.repository_interface.wallet_repository_interface import IWalletRepository
from infra.fee_strategy import IFeeStrategy


class ITransactionService(Protocol):
    def create_transaction(
        self, from_wallet: str, to_wallet: str, amount_btc: float
    ) -> None:
        pass

    def get_transactions(self, api_key: str) -> list[Any]:
        pass

    def get_wallet_transactions(self, api_key: str, address: str) -> list[Any]:
        pass

    def get_statistics(self) -> dict[str, Any]:
        pass


class TransactionService(ITransactionService):
    def __init__(
        self,
        transactions_repository: ITransactionRepository,
        fee_strategy: IFeeStrategy,
        wallets_repository: IWalletRepository,
    ):
        self.transactions_repository = transactions_repository
        self.fee_strategy = fee_strategy
        self.wallets_repository = wallets_repository

    def create_transaction(
        self, from_wallet: str, to_wallet: str, amount_btc: float
    ) -> None:
        if from_wallet == to_wallet:
            raise IntoSameWalletTransactionError

        # will throw WalletDoesNotExist if to_wallet does not exist
        self.wallets_repository.get_wallet(to_wallet)

        if self.wallets_repository.get_balance(from_wallet) < amount_btc:
            raise NotEnoughBalanceError

        from_wallet_owner = self.wallets_repository.get_user(from_wallet)
        to_wallet_owner = self.wallets_repository.get_user(to_wallet)
        transaction_fee = self.fee_strategy.calculate_transaction_fee(
            amount_btc, from_wallet_owner, to_wallet_owner
        )

        sent_amount = amount_btc - transaction_fee
        self.transactions_repository.create_transaction(
            from_wallet, to_wallet, sent_amount, transaction_fee
        )
        from_wallet_new_balance = (
            self.wallets_repository.get_balance(from_wallet) - amount_btc
        )
        to_wallet_new_balance = (
            self.wallets_repository.get_balance(to_wallet) + sent_amount
        )
        self.wallets_repository.change_balance(from_wallet, from_wallet_new_balance)
        self.wallets_repository.change_balance(to_wallet, to_wallet_new_balance)

    def get_transactions(self, api_key: str) -> list[Any]:
        lst = list()
        for w in self.wallets_repository.get_wallets(api_key):
            for t in self.transactions_repository.get_wallet_all_transactions(
                str(w.address)
            ):
                from_wallet_index = 0
                if t[from_wallet_index] == w.address:
                    lst.append(t)
        return lst

    def get_wallet_transactions(self, api_key: str, address: str) -> list[Any]:
        # will throw WalletDoesNotExist error if the wallet doesn't exist
        self.wallets_repository.get_wallet(address)

        lst = list()
        for t in self.transactions_repository.get_wallet_all_transactions(address):
            lst.append(t)
        return lst

    def get_statistics(self) -> dict[str, Any]:
        res = self.transactions_repository.get_statistics()
        return {
            "amount": res["transaction_total_number"],
            "sum": res["transaction_total_amount"],
        }
