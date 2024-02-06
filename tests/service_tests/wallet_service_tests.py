import pytest
from fastapi import HTTPException

from core.constants import BTC_STARTING_BALANCE, MAX_WALLETS, TEST_UUID
from core.services.wallet_service import WalletService
from core.wallet import WalletUSD
from core.walletToWalletUSDAdapter import WalletToUSDWalletAdapter
from infra.BTCtoUSDconverter import BTCtoUSDConverter
from infra.repository.wallet_repository import InMemoryWalletRepository


class StubConverter:
    def convert(self, wallet) -> WalletUSD:
        pass


def test_create_wallet_success():
    converter = BTCtoUSDConverter()
    walleter = WalletToUSDWalletAdapter(converter)
    wallet_repository = InMemoryWalletRepository(converter)

    wallet_service = WalletService(
        wallet_repository=wallet_repository, adapter=walleter
    )

    wallet = wallet_service.create_wallet(str(TEST_UUID))

    assert isinstance(wallet, WalletUSD)
    assert wallet.amount == BTC_STARTING_BALANCE
    assert wallet.api_key == TEST_UUID


def test_create_wallet_more_than_limit():
    converter = BTCtoUSDConverter()
    walleter = WalletToUSDWalletAdapter(converter)
    wallet_repository = InMemoryWalletRepository(converter)

    wallet_service = WalletService(
        wallet_repository=wallet_repository, adapter=walleter
    )

    for _ in range(MAX_WALLETS + 1):
        wallet_service.create_wallet(str(TEST_UUID))

    with pytest.raises(HTTPException):
        wallet_service.create_wallet(str(TEST_UUID))
