from typing import Protocol

from core.wallet import IWallet, WalletUSD
from infra.BTCtoUSDconverter import IBTCtoUSDConverter


class IWalletToWalletUSDAdapter(Protocol):
    def convert(self, wallet: IWallet) -> WalletUSD:
        pass


class WalletToUSDWalletAdapter(IWalletToWalletUSDAdapter):
    def __init__(self, converter: IBTCtoUSDConverter):
        self.converter = converter

    def convert(self, wallet: IWallet) -> WalletUSD:
        usd_value = self.converter.convert(wallet.amount)
        return WalletUSD(
            usd_amount=usd_value,
            api_key=wallet.api_key,
            address=wallet.address,
            amount=wallet.amount,
        )
