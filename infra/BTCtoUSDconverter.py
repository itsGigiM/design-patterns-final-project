import json
from typing import Protocol

import requests


class IBTCtoUSDConverter(Protocol):
    def convert(self, btc: float) -> float:
        pass


class BTCtoUSDConverter(IBTCtoUSDConverter):
    @staticmethod
    def __get_btc_price() -> float:
        url = "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {"symbol": "BTC", "convert": "USD"}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "55522910-a61e-423d-8220-9e93457e986c",
        }

        session = requests.Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            btc_price = data["data"]["BTC"]["quote"]["USD"]["price"]
            # print(f"{amount_btc} BTC is equivalent to ${usd_value:.2f} USD")
            return float(btc_price)
        except (
            requests.ConnectionError,
            requests.Timeout,
            requests.TooManyRedirects,
        ) as e:
            print(e)
            return -1.0

    def convert(self, btc: float) -> float:
        btc_price = self.__get_btc_price()
        return btc * float(btc_price)
