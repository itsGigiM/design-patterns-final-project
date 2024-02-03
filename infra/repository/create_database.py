from core.repository_interface.create_database_repository import ICreateDatabase
from core.repository_interface.database_executor_interface import IDatabaseExecutor


class CreateDatabase(ICreateDatabase):

    def __init__(self, db_connection: IDatabaseExecutor):
        self.conn = db_connection

    def drop_table(self) -> None:
        self.conn.execute_query("DROP TABLE IF EXISTS user")
        self.conn.execute_query("DROP TABLE IF EXISTS wallet")
        self.conn.execute_query("DROP TABLE IF EXISTS transaction")

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS user (
                email TEXT PRIMARY KEY
                )"""
        self.conn.execute_query(query)

        query = """
            CREATE TABLE IF NOT EXISTS wallet (
                user TEXT,
                address TEXT PRIMARY KEY,
                btc_balance number,
                FOREIGN KEY (user) REFERENCES user(email),

            )"""
        self.conn.execute_query(query)

        query = """
            CREATE TABLE IF NOT EXISTS transaction (
                from_wallet text,
                to_wallet text,
                amount number,
                fee number,
                total number,
                FOREIGN KEY (from_wallet) REFERENCES wallet(address),
                FOREIGN KEY (to_wallet) REFERENCES wallet(address)
            )"""
        self.conn.execute_query(query)
