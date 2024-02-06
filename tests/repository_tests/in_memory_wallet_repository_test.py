import uuid

import pytest

from infra.BTCtoUSDconverter import IBTCtoUSDConverter
from infra.repository.wallet_repository import InMemoryWalletRepository


class StubConverter(IBTCtoUSDConverter):
    def convert(self, btc: float) -> float:
        btc_price = 1000
        return btc * float(btc_price)


@pytest.fixture
def wallet_repo() -> InMemoryWalletRepository:
    converter = StubConverter()
    wallet_repo = InMemoryWalletRepository(converter)
    wallet_repo.create_table()
    return wallet_repo


def test_create_wallet(wallet_repo: InMemoryWalletRepository) -> None:
    user = str(uuid.uuid4())
    address = str(uuid.uuid4())
    btc_balance = 10
    assert wallet_repo.create_wallet(user, address, btc_balance) is True


def test_exists_wallet(wallet_repo: InMemoryWalletRepository) -> None:
    user = str(uuid.uuid4())
    address = str(uuid.uuid4())
    assert wallet_repo.exists_wallet(address) is False
    wallet_repo.create_wallet(user, address)
    assert wallet_repo.exists_wallet(address) is True


def test_change_balance(wallet_repo: InMemoryWalletRepository) -> None:
    user = str(uuid.uuid4())
    address = str(uuid.uuid4())
    wallet_repo.create_wallet(user, address, 2)
    wallet_repo.change_balance(address, 3)
    assert wallet_repo.get_balance(address) == 3


def test_get_balance(wallet_repo: InMemoryWalletRepository) -> None:
    user = str(uuid.uuid4())
    address = str(uuid.uuid4())
    wallet_repo.create_wallet(user, address)
    assert wallet_repo.get_balance(address) == 1


def test_get_user(wallet_repo: InMemoryWalletRepository) -> None:
    user = str(uuid.uuid4())
    address = str(uuid.uuid4())
    wallet_repo.create_wallet(user, address)
    assert wallet_repo.get_user(address) == user


def test_get_wallet(wallet_repo: InMemoryWalletRepository) -> None:
    user = str(uuid.uuid4())
    address = str(uuid.uuid4())
    wallet_repo.create_wallet(user, address)
    wallet = wallet_repo.get_wallet(address)
    assert str(wallet.api_key) == user
    assert str(wallet.address) == address
    assert wallet.amount == 1


def test_get_wallets(wallet_repo: InMemoryWalletRepository) -> None:
    user = str(uuid.uuid4())
    addresses = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
    for address in addresses:
        wallet_repo.create_wallet(user, address)
    wallets = wallet_repo.get_wallets(user)
    assert len(wallets) == len(addresses)
    for wallet in wallets:
        assert str(wallet.api_key) == user
        assert str(wallet.address) in addresses
