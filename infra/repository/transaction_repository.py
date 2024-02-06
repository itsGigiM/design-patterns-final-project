import uuid
from typing import Any

from core.exceptions import CanNotGetStatisticsError, CanNotGetTransactionsError
from core.repository_interface.create_database_repository import ICreateDatabase
from core.repository_interface.database_executor_interface import IDatabaseExecutor
from core.repository_interface.transaction_repository_interface import (
    ITransactionRepository,
)
from core.transaction import Transaction


class SQLTransactionRepository(ITransactionRepository, ICreateDatabase):
    def __init__(self, db_connection: IDatabaseExecutor):
        self.conn = db_connection
        # self.drop_table()
        self.create_table()

    def drop_table(self) -> None:
        self.conn.execute_query("DROP TABLE IF EXISTS transactions")

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS transactions (
                from_wallet text,
                to_wallet text,
                amount number,
                fee number,
                total number,
                FOREIGN KEY (from_wallet) REFERENCES wallet(address),
                FOREIGN KEY (to_wallet) REFERENCES wallet(address)
            )"""
        self.conn.execute_query(query)

    def create_transaction(
        self, from_wallet: str, to_wallet: str, sent_amount: float, fee_amount: float
    ) -> bool:
        query = (
            "INSERT INTO transactions(from_wallet, to_wallet, amount, fee, total) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        params = (
            from_wallet,
            to_wallet,
            sent_amount,
            fee_amount,
            fee_amount + sent_amount,
        )
        if self.conn.execute_query(query, params) == 0:
            return False
        self.conn.commit()
        return True

    def get_all_transactions(self) -> Any:
        select_query = "SELECT * FROM transactions"
        transactions = self.conn.search(select_query)
        if transactions is None:
            raise CanNotGetTransactionsError.custom_exception()
        return transactions

    def get_wallet_all_transactions(self, wallet: str) -> Any:
        select_query = (
            "SELECT * FROM transactions WHERE from_wallet = ? or to_wallet = ?"
        )
        transactions = self.conn.search(select_query, (wallet, wallet))
        if transactions is None:
            raise CanNotGetTransactionsError.custom_exception()
        return transactions

    def get_statistics(self) -> dict[str, float]:
        select_query = "SELECT SUM(total), COUNT(*) FROM transactions"
        res = self.conn.search(select_query)[0]
        if res is None:
            raise CanNotGetStatisticsError.custom_exception()
        return {"transaction_total_number": res[1], "transaction_total_amount": res[0]}


class InMemoryTransactionRepository(ITransactionRepository, ICreateDatabase):
    transactions: list[Transaction] = []

    def drop_table(self) -> None:
        self.transactions.clear()

    def create_table(self) -> None:
        self.transactions.clear()

    def create_transaction(
        self, from_wallet: str, to_wallet: str, sent_amount: float, fee_amount: float
    ) -> bool:
        total_amount = sent_amount + fee_amount
        from_wallet_uuid = from_wallet
        to_wallet_uuid = to_wallet
        new_transaction = Transaction(
            uuid.UUID(from_wallet_uuid),
            uuid.UUID(to_wallet_uuid),
            sent_amount,
            fee_amount,
            total_amount,
        )
        self.transactions.append(new_transaction)
        return True

    def get_all_transactions(self) -> Any:
        return self.transactions

    def get_wallet_all_transactions(self, wallet: str) -> Any:
        transactions_list = []
        for transaction in self.transactions:
            is_from_wallet = str(transaction.from_wallet_address) == wallet
            is_to_wallet = str(transaction.to_wallet_address) == wallet
            if is_from_wallet or is_to_wallet:
                transactions_list.append(transaction)
        return transactions_list

    def get_statistics(self) -> dict[str, float]:
        total_profit: float = 0
        for transaction in self.transactions:
            total_profit += transaction.fee_amount + transaction.sent_amount
        return {
            "transaction_total_number": len(self.transactions),
            "transaction_total_amount": total_profit,
        }
