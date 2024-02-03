from typing import Any, Optional, Tuple

from core.repository_interface.database_connection_interface import IDatabaseConnection
from core.repository_interface.database_executor_interface import IDatabaseExecutor


class DatabaseExecutor(IDatabaseExecutor):
    def __init__(self, connection: IDatabaseConnection):
        self.connection = connection
        self.conn = connection.get_connection()

    def execute_query(self, q: str, p: Optional[Tuple[Any]] = None) -> int:
        with self.conn:
            cursor = self.conn.cursor()
            if p:
                return cursor.execute(q, p).rowcount
            else:
                return cursor.execute(q).rowcount

    def search(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Any:
        with self.conn:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def commit(self) -> None:
        self.conn.commit()
