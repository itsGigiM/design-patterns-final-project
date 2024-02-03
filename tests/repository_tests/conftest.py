from typing import Generator

import pytest

from infra.repository.database_connection import DatabaseConnection
from infra.repository.database_executor import DatabaseExecutor

TEST_DB_NAME = ":memory:"


@pytest.fixture
def db_connection() -> Generator[DatabaseConnection, None, None]:
    connection = DatabaseConnection(db_name=TEST_DB_NAME)
    yield connection
    connection.conn.close()


@pytest.fixture
def db_executor(db_connection: DatabaseConnection) -> DatabaseExecutor:
    executor = DatabaseExecutor(connection=db_connection)
    return executor
