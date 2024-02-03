from sqlite3 import Connection
from typing import Protocol


class IDatabaseConnection(Protocol):
    def create_connection(self) -> Connection:
        pass

    def get_connection(self) -> Connection:
        pass
