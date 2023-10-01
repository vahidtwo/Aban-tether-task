from decimal import Decimal

from apps.coin.models import Coin
from apps.exchange.integration import ResultOfExchange
from apps.exchange.integration.exception import ExchangeNotFound
from apps.exchange.integration.exchange_schema import (
    ExchangeABC,
    ExchangeManagerABC,
)
from config import env

# TODO it must be replace all exchangeABC functions to async


class BinanceExchange(ExchangeABC):
    api_key = env("binance_exchange_api_key", default="")
    gate_way = "https://api.binance.com"

    def transfer(self, to_wallet: str, amount: Decimal, currency: str) -> ResultOfExchange:
        """transfer amount of a currency from one wallet to another wallet"""
        print(f"transfer {amount}[{currency}] to wallet {to_wallet} from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")

    def buy(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        print(f"buy {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")

    def sell(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        print(f"sell {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")


class CoinBaseExchange(ExchangeABC):
    api_key = env("coinbase_exchange_api_key", default="")
    gate_way = "https://api.coinbase.com"

    def transfer(self, to_wallet: str, amount: Decimal, currency: str) -> ResultOfExchange:
        """transfer amount of a currency from one wallet to another wallet"""
        print(f"transfer {amount}[{currency}] to wallet {to_wallet} from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")

    def buy(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        print(f"buy {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")

    def sell(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        print(f"sell {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")


class KuCoinExchange(ExchangeABC):
    api_key = env("kocoin_exchange_api_key", default="")
    gate_way = "https://api.kocoin.com"

    def transfer(self, to_wallet: str, amount: Decimal, currency: str) -> ResultOfExchange:
        """transfer amount of a currency from one wallet to another wallet"""
        print(f"transfer {amount}[{currency}] to wallet {to_wallet} from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")

    def buy(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        print(f"buy {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")

    def sell(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        print(f"sell {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status_code=200, result_message="ok")


class ExchangeManager(ExchangeManagerABC):
    """
    Exchange Manager for managing exchanges based on coins.

    This class provides methods for transferring, buying, and selling cryptocurrency on the appropriate exchange
     based on the coin provided.
    usage:
        get exchange
        >>> ExchangeManager.get_exchange_from_coins(coin=coin)
        buy currency
        >>> ExchangeManager(coin).buy(Decimal(10.2))
        sell currency
        >>> ExchangeManager(coin).sell(Decimal(10.2))
        transfer currency
        >>> ExchangeManager(coin).transfer(to_wallet=user_wallet, amount=Decimal(10.2))
    """

    @staticmethod
    def get_exchange_from_coins(coin: Coin) -> ExchangeABC:
        """return exchange class according to given coin"""
        if coin.exchange is None:
            # TODO it could be implement in local network or handle it by business, ask about it for implementation
            raise ExchangeNotFound(f"exchange is empty for {coin.name}")
        match coin.exchange:
            case "binance":
                return BinanceExchange()
            case "coinbase":
                return CoinBaseExchange()
            case "kucoin":
                return KuCoinExchange()
            case _:
                raise ExchangeNotFound(f"exchange not found for this coin {coin.name}")
