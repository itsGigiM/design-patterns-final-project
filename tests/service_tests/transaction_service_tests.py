from core.services.transaction_service import TransactionService
from infra.BTCtoUSDconverter import BTCtoUSDConverter
from infra.fee_strategy import FeeStrategy
from infra.repository.transaction_repository import InMemoryTransactionRepository
from infra.repository.wallet_repository import InMemoryWalletRepository

TRANSACTION_REPO = InMemoryTransactionRepository()
FREE_STRATEGY = FeeStrategy()
CONVERTER = BTCtoUSDConverter()
WALLETS_REPO = InMemoryWalletRepository(CONVERTER)

FROM = "12345678-1234-5678-1234-567812345678"
TO = "87654321-4321-6789-4321-987654321098"

SERVICE = TransactionService(transactions_repository=TRANSACTION_REPO,
                             fee_strategy=FREE_STRATEGY, wallets_repository=WALLETS_REPO)


def test_create_transaction():
    WALLETS_REPO.create_table()
    WALLETS_REPO.create_wallet(FROM, FROM, 1000)
    WALLETS_REPO.create_wallet(TO, TO, 1000)
    SERVICE.create_transaction(FROM, TO, 100)


def test_get_transactions():
    WALLETS_REPO.create_table()
    WALLETS_REPO.create_wallet(FROM, FROM, 1000)
    WALLETS_REPO.create_wallet(TO, TO, 1000)
    SERVICE.create_transaction(FROM, TO, 100)
    transactions = SERVICE.get_transactions(FROM)
    found_transaction = False
    for cur in transactions:
        if str(cur.from_wallet_address) == FROM:
            assert cur.sent_amount + cur.fee_amount == 100
            found_transaction = True
    assert found_transaction is True


def test_get_wallet_transactions():
    WALLETS_REPO.create_table()
    WALLETS_REPO.create_wallet(FROM, FROM, 1000)
    WALLETS_REPO.create_wallet(TO, TO, 1000)
    SERVICE.create_transaction(FROM, TO, 100)
    SERVICE.create_transaction(TO, FROM, 50)

    from_wallet_transactions = SERVICE.get_wallet_transactions(FROM, FROM)
    to_wallet_transactions = SERVICE.get_wallet_transactions(TO, TO)

    assert any(str(t.from_wallet_address) == FROM for t in from_wallet_transactions)
    assert any(str(t.to_wallet_address) == TO for t in to_wallet_transactions)


def test_get_statistics():
    WALLETS_REPO.drop_table()
    WALLETS_REPO.create_table()
    TRANSACTION_REPO.drop_table()
    WALLETS_REPO.create_wallet(FROM, FROM, 1000)
    WALLETS_REPO.create_wallet(TO, TO, 1000)

    SERVICE.create_transaction(FROM, TO, 100)
    SERVICE.create_transaction(TO, FROM, 50)
    stats = SERVICE.get_statistics()

    assert stats["amount"] == 2
    assert stats["sum"] == 150
