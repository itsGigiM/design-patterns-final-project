import pytest

from infra.repository.database_executor import DatabaseExecutor
from infra.repository.transaction_repository import SQLTransactionRepository


@pytest.fixture
def transaction_repo(db_executor: DatabaseExecutor) -> SQLTransactionRepository:
    transaction_repo = SQLTransactionRepository(db_connection=db_executor)
    transaction_repo.create_table()
    return transaction_repo


def test_create_Transaction(transaction_repo: SQLTransactionRepository) -> None:
    assert transaction_repo.create_transaction("from", "to", 100, 5)


def test_get_all_transactions(transaction_repo: SQLTransactionRepository) -> None:
    result = transaction_repo.get_all_transactions()
    assert result == []
    transaction_repo.create_transaction("from", "to", 100, 5)
    transaction_repo.create_transaction("from", "to", 20, 5)
    result = transaction_repo.get_all_transactions()
    assert result == [("from", "to", 100, 5, 105), ("from", "to", 20, 5, 25)]


def test_get_wallet_all_transactions(
    transaction_repo: SQLTransactionRepository,
) -> None:
    result = transaction_repo.get_wallet_all_transactions("to")
    assert result == []
    transaction_repo.create_transaction("from", "to", 100, 5)
    transaction_repo.create_transaction("from", "to", 20, 5)
    result = transaction_repo.get_wallet_all_transactions("to")
    assert result == [("from", "to", 100, 5, 105), ("from", "to", 20, 5, 25)]


def test_get_statistics(transaction_repo: SQLTransactionRepository) -> None:
    transaction_repo.create_transaction("from", "to", 100, 5)
    transaction_repo.create_transaction("from", "to", 20, 5)
    result = transaction_repo.get_statistics()
    assert result == {"transaction_total_number": 2, "transaction_total_amount": 130}
