from typing import Any

from core.repository_interface.create_database_repository import ICreateDatabase
from core.repository_interface.database_executor_interface import IDatabaseExecutor
from core.repository_interface.user_repository_interface import IUserRepository


class SQLUserRepository(IUserRepository, ICreateDatabase):
    def __init__(self, db_connection: IDatabaseExecutor):
        self.conn = db_connection
        self.drop_table()
        self.create_table()

    def drop_table(self) -> None:
        self.conn.execute_query("DROP TABLE IF EXISTS user")

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS user (
                email TEXT PRIMARY KEY,
                wallet_number int
                )"""
        self.conn.execute_query(query)

    def create_user(self, email: str) -> str:
        query = "INSERT INTO user (email, wallet_number) VALUES (?, ?)"
        params = (email, 0)
        if self.conn.execute_query(query, params) == 0:
            return ""
        self.conn.commit()
        return email

    def exists_user(self, email: str) -> bool:
        select_query = "SELECT * FROM user WHERE LOWER(email) = LOWER(?)"
        existing_unit = self.conn.search(select_query, params=(email,))
        return bool(existing_unit)

    def set_wallet_number(self, email: str, wallet_num: int) -> None:
        query = "UPDATE user SET wallet_number = ? WHERE email = ?"
        params = (str(wallet_num), email)
        if self.conn.execute_query(query, params) == 0:
            raise Exception("Cannot update the user wallet number")
        self.conn.commit()

    def get_wallet_number(self, email: str) -> Any:
        select_query = "SELECT wallet_number FROM user WHERE LOWER(email) = LOWER(?)"
        res = self.conn.search(select_query, params=(email,))
        return res[0][0]


class InMemoryUserRepository(IUserRepository, ICreateDatabase):
    memory_dict: dict[Any, Any]

    def __init__(self) -> None:
        self.memory_dict = {}

    def create_user(self, email: str) -> str:
        if self.exists_user(email):
            raise Exception("User already exists")
        self.memory_dict[email] = 0
        return email

    def exists_user(self, email: str) -> bool:
        return email in self.memory_dict

    def set_wallet_number(self, email: str, wallet_num: int) -> None:
        if not self.exists_user(email):
            raise Exception("Cannot find user with this email")
        self.memory_dict[email] = wallet_num

    def get_wallet_number(self, email: str) -> Any:
        if not self.exists_user(email):
            raise Exception("Cannot find user with this email")
        return self.memory_dict[email]
