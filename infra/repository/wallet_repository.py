import copy
import uuid
from typing import Any

from core.exceptions import (
    CanNotGetUserError,
    CanNotGetWalletBalanceError,
    CanNotUpdateWalletBalanceError,
    WalletDoesNotExistError,
)
from core.repository_interface.create_database_repository import ICreateDatabase
from core.repository_interface.database_executor_interface import IDatabaseExecutor
from core.repository_interface.wallet_repository_interface import IWalletRepository
from core.wallet import Wallet
from infra.BTCtoUSDconverter import IBTCtoUSDConverter


class InMemoryWalletRepository(IWalletRepository, ICreateDatabase):
    wallets: dict[str, Wallet]
    converter: IBTCtoUSDConverter

    def __init__(self, converter: IBTCtoUSDConverter):
        self.converter = converter
        self.wallets: dict[str, Wallet] = dict()

    def drop_table(self) -> None:
        self.wallets = {}

    def create_table(self) -> None:
        self.wallets: dict[str, Wallet] = dict()

    def create_wallet(self, user: str, address: str, btc_balance: float = 1) -> bool:
        new_wallet = Wallet(
            address=uuid.UUID(address), amount=btc_balance, api_key=uuid.UUID(user)
        )
        self.wallets[address] = new_wallet
        return True

    def exists_wallet(self, address: str) -> bool:
        return address in self.wallets

    def change_balance(self, address: str, balance_change: float) -> None:
        wallet = self.wallets[address]
        wallet.amount = balance_change

    def get_balance(self, address: str) -> float:
        return self.wallets[address].amount

    def get_user(self, address: str) -> str:
        return str(self.wallets[address].api_key)

    def get_wallet(self, address: str) -> Wallet:
        if address in self.wallets:
            our_wallet = self.wallets[address]
            return copy.copy(our_wallet)

        raise WalletDoesNotExistError.custom_exception()

    def get_wallets(self, api_key: str) -> list[Wallet]:
        lst = []
        for address, wallet in self.wallets.items():
            if str(wallet.api_key) == api_key:
                lst.append(wallet)
        return lst


class SQLWalletRepository(IWalletRepository, ICreateDatabase):
    def __init__(self, db_connection: IDatabaseExecutor):
        self.conn = db_connection
        # self.drop_table()
        self.create_table()

    def drop_table(self) -> None:
        self.conn.execute_query("DROP TABLE IF EXISTS wallet")

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS wallet (
                api_key TEXT,
                address TEXT PRIMARY KEY,
                btc_balance number,
                FOREIGN KEY (api_key) REFERENCES user(email)
            )"""
        self.conn.execute_query(query)

    def create_wallet(self, api_key: str, address: str, btc_balance: float = 1) -> bool:
        query = "INSERT INTO wallet(api_key, address, btc_balance) VALUES (?, ?, ?)"
        params = (api_key, address, btc_balance)
        if self.conn.execute_query(query, params) == 0:
            return False
        self.conn.commit()
        return True

    def exists_wallet(self, address: str) -> bool:
        select_query = "SELECT * FROM wallet WHERE LOWER(address) = LOWER(?)"
        existing_unit = self.conn.search(select_query, params=(address,))
        return bool(existing_unit)

    def change_balance(self, address: str, balance_change: float) -> None:
        query = "UPDATE wallet SET btc_balance = ? WHERE address = ?"
        params = (str(balance_change), address)
        if self.conn.execute_query(query, params) == 0:
            raise CanNotUpdateWalletBalanceError.custom_exception()
        self.conn.commit()

    def get_balance(self, address: str) -> Any:
        select_query = "SELECT btc_balance FROM wallet WHERE address = ?"
        data = self.conn.search(select_query, (address,))
        if data is None:
            raise CanNotGetWalletBalanceError.custom_exception()
        return data[0][0]

    def get_user(self, address: str) -> Any:
        select_query = "SELECT api_key FROM wallet WHERE address = ?"
        data = self.conn.search(select_query, (address,))
        if data is None:
            raise CanNotGetUserError.custom_exception()
        return data[0][0]

    def get_wallet(self, address: str) -> Wallet:
        select_query = "SELECT * FROM wallet WHERE address = ?"
        wallet = self.conn.search(select_query, (address,))
        if len(wallet) == 0:
            raise WalletDoesNotExistError.custom_exception()
        w = wallet[0]
        return Wallet(w[1], w[0], w[2])

    def get_wallets(self, api_key: str) -> list[Wallet]:
        select_query = "SELECT * FROM wallet WHERE api_key = ?"
        wallets = self.conn.search(select_query, (api_key,))
        if wallets is None:
            raise WalletDoesNotExistError.custom_exception()
        lst = list()
        for w in wallets:
            lst.append(Wallet(w[1], w[0], w[2]))
        return lst
