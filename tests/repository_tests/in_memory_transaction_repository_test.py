from typing import Any

import pytest

from infra.repository.database_executor import DatabaseExecutor
from infra.repository.transaction_repository import InMemoryTransactionRepository


@pytest.fixture
def transaction_repo(db_executor: DatabaseExecutor) -> InMemoryTransactionRepository:
    transaction_repo = InMemoryTransactionRepository()
    transaction_repo.create_table()
    return transaction_repo


valid_uuid1 = "12345678-1234-5678-1234-567812345678"
valid_uuid2 = "87654321-4321-6789-4321-987654321098"


def test_create_Transaction(transaction_repo: InMemoryTransactionRepository) -> None:
    assert transaction_repo.create_transaction(valid_uuid1, valid_uuid2, 100, 5)


def compare(result: Any):
    expected_results = [
        (valid_uuid1, valid_uuid2, 100, 5, 105),
        (valid_uuid1, valid_uuid1, 20, 5, 25)
    ]

    assert len(result) == len(expected_results)
    for transaction, expected in zip(result, expected_results):
        assert str(transaction.from_wallet_address) == expected[0]
        assert str(transaction.to_wallet_address) == expected[1]
        assert transaction.sent_amount == expected[2]
        assert transaction.fee_amount == expected[3]
        assert transaction.total_amount == expected[4]


def test_get_all_transactions(transaction_repo: InMemoryTransactionRepository) -> None:
    result = transaction_repo.get_all_transactions()
    assert result == []

    transaction_repo.create_transaction(valid_uuid1, valid_uuid2, 100, 5)
    transaction_repo.create_transaction(valid_uuid1, valid_uuid1, 20, 5)

    result = transaction_repo.get_all_transactions()

    assert len(result) == 2

    # Check details of the first transaction
    assert str(result[0].from_wallet_address) == valid_uuid1
    assert str(result[0].to_wallet_address) == valid_uuid2
    assert result[0].sent_amount == 100
    assert result[0].fee_amount == 5
    assert result[0].total_amount == 105

    # Check details of the second transaction
    assert str(result[1].from_wallet_address) == valid_uuid1
    assert str(result[1].to_wallet_address) == valid_uuid1
    assert result[1].sent_amount == 20
    assert result[1].fee_amount == 5
    assert result[1].total_amount == 25


def test_get_wallet_all_transactions(
        transaction_repo: InMemoryTransactionRepository,
) -> None:
    result = transaction_repo.get_wallet_all_transactions(valid_uuid2)
    assert result == []
    transaction_repo.create_transaction(valid_uuid1, valid_uuid2, 100, 5)
    transaction_repo.create_transaction(valid_uuid1, valid_uuid2, 20, 5)
    result = transaction_repo.get_wallet_all_transactions(valid_uuid2)
    compare(result)


def test_get_statistics(transaction_repo: InMemoryTransactionRepository) -> None:
    transaction_repo.drop_table()
    transaction_repo.create_table()
    transaction_repo.create_transaction(valid_uuid1, valid_uuid2, 100, 5)  # Total amount 105, fee 5
    transaction_repo.create_transaction(valid_uuid1, valid_uuid2, 20, 5)  # Total amount 25, fee 5
    result = transaction_repo.get_statistics()

    assert result["transaction_total_number"] == 2
    assert result["transaction_total_amount"] == 10
