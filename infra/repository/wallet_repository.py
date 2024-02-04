import copy
from typing import Any, Optional

from core.BTCtoUSDconverter import IBTCtoUSDConverter
from core.repository_interface.create_database_repository import ICreateDatabase
from core.repository_interface.database_executor_interface import IDatabaseExecutor
from core.repository_interface.wallet_repository_interface import IWalletRepository
from core.wallet import Wallet


class InMemoryWalletRepository(IWalletRepository, ICreateDatabase):

    wallets: dict[str, Wallet]
    converter: IBTCtoUSDConverter

    def __init__(self, converter: IBTCtoUSDConverter):
        self.converter = converter

    def drop_table(self) -> None:
        wallets = None

    def create_table(self) -> None:
        wallets: dict[str, Wallet] = dict()

    def create_wallet(self, user: str, address: str, btc_balance: int = 1) -> bool:
        new_wallet = Wallet(address=address, amount=btc_balance, api_key=user)
        self.wallets[address] = new_wallet

    def exists_wallet(self, address: str) -> bool:
        return address in self.wallets

    def change_balance(self, address: str, balance_change: int) -> None:
        wallet = self.wallets[address]
        wallet.amount = balance_change

    def get_balance(self, address: str) -> int:
        return self.wallets[address].amount

    def get_user(self, address: str) -> str:
        return self.wallets[address].api_key

    def get_wallet(self, address: str) -> Optional[Any]:
        our_wallet = self.wallets[address]
        return copy.copy(our_wallet)

    def get_wallets(self, user: str) -> Any:
        lst = list()
        for address, wallet in self.wallets.items():
            if wallet.api_key == user:
                lst.append(wallet)
        return lst


class SQLWalletRepository(IWalletRepository, ICreateDatabase):
    def __init__(self, db_connection: IDatabaseExecutor):
        self.conn = db_connection
        self.drop_table()
        self.create_table()

    def drop_table(self) -> None:
        self.conn.execute_query("DROP TABLE IF EXISTS wallet")

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS wallet (
                user_id TEXT,
                address TEXT PRIMARY KEY,
                btc_balance number,
                FOREIGN KEY (user_id) REFERENCES user(email)
            )"""
        self.conn.execute_query(query)

    def create_wallet(self, user_id: str, address: str, btc_balance: int = 1) -> bool:
        query = "INSERT INTO wallet(user_id, address, btc_balance) VALUES (?, ?, ?)"
        params = (user_id, address, btc_balance)
        if self.conn.execute_query(query, params) == 0:
            return False
        self.conn.commit()
        return True

    def exists_wallet(self, address: str) -> bool:
        select_query = "SELECT * FROM wallet WHERE LOWER(address) = LOWER(?)"
        existing_unit = self.conn.search(select_query, params=(address,))
        return bool(existing_unit)

    def change_balance(self, address: str, balance_change: int) -> None:
        query = "UPDATE wallet SET btc_balance = ? WHERE address = ?"
        params = (str(balance_change), address)
        if self.conn.execute_query(query, params) == 0:
            raise Exception("Cannot update the btc balance in wallet")
        self.conn.commit()

    def get_balance(self, address: str) -> Any:
        select_query = "SELECT btc_balance FROM wallet WHERE address = ?"
        data = self.conn.search(select_query, (address,))
        if data is None:
            raise Exception("Could not get balance for the wallet")
        return data[0][0]

    def get_user(self, address: str) -> str:
        select_query = "SELECT user_id FROM wallet WHERE address = ?"
        data = self.conn.search(select_query, (address,))
        if data is None:
            raise Exception("Could not get user for the wallet")
        return data[0][0]

    def get_wallet(self, address: str) -> Optional[Any]:
        select_query = "SELECT * FROM wallet WHERE address = ?"
        wallet = self.conn.search(select_query, (address,))
        if wallet is None:
            raise Exception("Could not get balance for the wallet")
        return wallet[0]

    def get_wallets(self, user_id: str) -> Any:
        select_query = "SELECT * FROM wallet WHERE user_id = ?"
        wallets = self.conn.search(select_query, (user_id,))
        if wallets is None:
            raise Exception("Could not get balance for the wallet")
        return wallets
