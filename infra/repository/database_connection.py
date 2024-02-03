import sqlite3
from sqlite3 import Connection, Error

from core.repository_interface.database_connection_interface import IDatabaseConnection


class DatabaseConnection(IDatabaseConnection):
    def __init__(self, db_name: str = "bitcoin_wallet_db") -> None:
        self.db_name = db_name
        self.conn = self.create_connection()

    def create_connection(self) -> Connection:
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except Error:
            raise Exception("Cannot connect to database")

    def get_connection(self) -> Connection:
        return self.conn