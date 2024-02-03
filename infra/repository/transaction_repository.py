from typing import Any

from core.repository_interface.create_database_repository import ICreateDatabase
from core.repository_interface.database_executor_interface import IDatabaseExecutor
from core.repository_interface.transaction_repository_interface import (
    ITransactionRepository,
)


class SQLTransactionRepository(ITransactionRepository, ICreateDatabase):
    def __init__(self, db_connection: IDatabaseExecutor):
        self.conn = db_connection
        self.drop_table()
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

    def create_Transaction(
        self, from_wallet: str, to_wallet: str, sent_amount: int, fee_amount: int
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
            raise Exception("Could not get balance for the wallet")
        return transactions

    def get_wallet_all_transactions(self, wallet: str) -> Any:
        select_query = (
            "SELECT * FROM transactions WHERE from_wallet = ? or to_wallet = ?"
        )
        transactions = self.conn.search(select_query, (wallet, wallet))
        if transactions is None:
            raise Exception("Could not get balance for the wallet")
        return transactions

    def get_statistics(self) -> dict[str, int]:
        select_query = "SELECT SUM(total), COUNT(*) FROM transactions"
        res = self.conn.search(select_query)[0]
        if res is None:
            raise Exception("Could not get balance for the wallet")
        return {"transaction_total_number": res[1], "transaction_total_amount": res[0]}