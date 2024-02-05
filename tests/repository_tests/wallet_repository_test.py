import pytest

from infra.repository.database_executor import DatabaseExecutor
from infra.repository.wallet_repository import SQLWalletRepository


@pytest.fixture
def wallet_repo(db_executor: DatabaseExecutor) -> SQLWalletRepository:
    user_db = SQLWalletRepository(db_connection=db_executor)
    user_db.create_table()
    return user_db


def test_create_wallet(wallet_repo: SQLWalletRepository) -> None:
    user = "user1"
    address = "wallet_address1"
    btc_balance = 10
    assert wallet_repo.create_wallet(user, address, btc_balance) is True


def test_create_existing_wallet(wallet_repo: SQLWalletRepository) -> None:
    user = "user2"
    address = "wallet_address2"
    assert wallet_repo.create_wallet(user, address) is True
    with pytest.raises(Exception):
        wallet_repo.create_wallet(user, address)


def test_exists_wallet(wallet_repo: SQLWalletRepository) -> None:
    address = "wallet_address3"
    assert wallet_repo.exists_wallet(address) is False
    wallet_repo.create_wallet("user3", address)
    assert wallet_repo.exists_wallet(address) is True


def test_change_balance(wallet_repo: SQLWalletRepository) -> None:
    address = "wallet_address4"
    wallet_repo.create_wallet("user4", address, 2)
    wallet_repo.change_balance(address, 3)
    assert wallet_repo.get_balance(address) == 3


def test_get_balance(wallet_repo: SQLWalletRepository) -> None:
    address = "wallet_address5"
    wallet_repo.create_wallet("user5", address)
    assert wallet_repo.get_balance(address) == 1


def test_get_user(wallet_repo: SQLWalletRepository) -> None:
    address = "wallet_address5"
    wallet_repo.create_wallet("user5", address)
    assert wallet_repo.get_user(address) == "user5"


def test_get_wallet(wallet_repo: SQLWalletRepository) -> None:
    address = "wallet_address6"
    user = "user6"
    wallet_repo.create_wallet(user, address)
    wallet = wallet_repo.get_wallet(address)
    assert wallet.api_key == user
    assert wallet.address == address
    assert wallet.amount == 1


def test_get_wallets(wallet_repo: SQLWalletRepository) -> None:
    user = "user"
    addresses = ["1", "2", "3"]
    for address in addresses:
        wallet_repo.create_wallet(user, address)
    wallets = wallet_repo.get_wallets(user)
    assert len(wallets) == len(addresses)
    for wallet in wallets:
        assert wallet.api_key == user
        assert wallet.address in addresses
