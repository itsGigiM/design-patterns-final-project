from typing import Protocol

from core.BTCtoUSDconverter import IBTCtoUSDConverter
from core.wallet import Wallet, WalletUSD


class IWalletToWalletUSDAdapter(Protocol):
    def convert(self, wallet: Wallet) -> WalletUSD:
        pass


class WalletToUSDWalletAdapter(IWalletToWalletUSDAdapter):
    def __init__(self, converter: IBTCtoUSDConverter):
        self.converter = converter

    def convert(self, wallet: Wallet) -> WalletUSD:
        usd_value = self.converter.convert(wallet.amount)
        usd_wallet = WalletUSD(usd_amount=usd_value, api_key=wallet.api_key ,address=wallet.address, btc_amount=wallet.amount)

