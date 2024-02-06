from typing import Any

import pytest

from infra.repository.transaction_repository import InMemoryTransactionRepository


@pytest.fixture
def transaction_repo() -> InMemoryTransactionRepository:
    transaction_repo = InMemoryTransactionRepository()
    transaction_repo.create_table()
    return transaction_repo


FROM = "12345678-1234-5678-1234-567812345678"
TO = "87654321-4321-6789-4321-987654321098"


def test_create_transaction(transaction_repo: InMemoryTransactionRepository) -> None:
    assert transaction_repo.create_transaction(FROM, TO, 100, 5)


def test_get_all_transactions(transaction_repo: InMemoryTransactionRepository) -> None:
    result = transaction_repo.get_all_transactions()
    assert result == []

    transaction_repo.create_transaction(FROM, TO, 100, 5)
    transaction_repo.create_transaction(FROM, FROM, 20, 5)

    result = transaction_repo.get_all_transactions()

    assert len(result) == 2

    # Check details of the first transaction
    assert str(result[0].from_wallet_address) == FROM
    assert str(result[0].to_wallet_address) == TO
    assert result[0].sent_amount == 100
    assert result[0].fee_amount == 5
    assert result[0].total_amount == 105

    # Check details of the second transaction
    assert str(result[1].from_wallet_address) == FROM
    assert str(result[1].to_wallet_address) == FROM
    assert result[1].sent_amount == 20
    assert result[1].fee_amount == 5
    assert result[1].total_amount == 25


def test_get_wallet_all_transactions(
        transaction_repo: InMemoryTransactionRepository,
) -> None:
    result = transaction_repo.get_wallet_all_transactions(TO)
    assert result == []
    transaction_repo.create_transaction(FROM, TO, 100, 5)
    transaction_repo.create_transaction(FROM, TO, 20, 5)
    result = transaction_repo.get_wallet_all_transactions(TO)
    expected_results = [
        (FROM, TO, 100, 5, 105),
        (FROM, TO, 20, 5, 25)
    ]

    assert len(result) == len(expected_results)
    for transaction, expected in zip(result, expected_results):
        assert str(transaction.from_wallet_address) == expected[0]
        assert str(transaction.to_wallet_address) == expected[1]
        assert transaction.sent_amount == expected[2]
        assert transaction.fee_amount == expected[3]
        assert transaction.total_amount == expected[4]


def test_get_statistics(transaction_repo: InMemoryTransactionRepository) -> None:
    transaction_repo.drop_table()
    transaction_repo.create_table()
    transaction_repo.create_transaction(FROM, TO, 100, 5)  # Total amount 105, fee 5
    transaction_repo.create_transaction(FROM, TO, 20, 5)  # Total amount 25, fee 5
    result = transaction_repo.get_statistics()

    assert result["transaction_total_number"] == 2
    assert result["transaction_total_amount"] == 10
