import uuid

from core.constants import BTC_STARTING_BALANCE
from core.wallet import Wallet
from core.walletToWalletUSDAdapter import WalletToUSDWalletAdapter
from infra.BTCtoUSDconverter import BTCtoUSDConverter


def test_convert() -> None:
    wallet = Wallet(
        address=uuid.uuid4(), api_key=uuid.uuid4(), amount=BTC_STARTING_BALANCE
    )
    adapter = WalletToUSDWalletAdapter(BTCtoUSDConverter())
    walletUSD = adapter.convert(wallet)
    assert wallet.amount == walletUSD.amount
    assert wallet.api_key == walletUSD.api_key
    assert wallet.address == walletUSD.address
