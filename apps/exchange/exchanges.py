from typing import Type

from apps.exchange.exchange_schema import ExchangeABC, ResultOfExchange, ExchangeManagerABC, ExchangeNotFound
from config import env


class BinanceExchange(ExchangeABC):
    api_key = env("binance_exchange_api_key")
    gate_way = "https://api.binance.com"

    def transfer(self, to_wallet: str, amount: float, currency: str) -> ResultOfExchange:
        """transfer amount of a currency from one wallet to another wallet"""
        print(f"transfer {amount}[{currency}] to wallet {to_wallet} from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")

    def buy(self, amount: float, currency: str) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        print(f"buy {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")

    def sell(self, amount: float, currency: str) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        print(f"sell {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")


class CoinBaseExchange(ExchangeABC):
    api_key = env("coinbase_exchange_api_key")
    gate_way = "https://api.coinbase.com"

    def transfer(self, to_wallet: str, amount: float, currency: str) -> ResultOfExchange:
        """transfer amount of a currency from one wallet to another wallet"""
        print(f"transfer {amount}[{currency}] to wallet {to_wallet} from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")

    def buy(self, amount: float, currency: str) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        print(f"buy {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")

    def sell(self, amount: float, currency: str) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        print(f"sell {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")


class KuCoinExchange(ExchangeABC):
    api_key = env("kocoin_exchange_api_key")
    gate_way = "https://api.kocoin.com"

    def transfer(self, to_wallet: str, amount: float, currency: str) -> ResultOfExchange:
        """transfer amount of a currency from one wallet to another wallet"""
        print(f"transfer {amount}[{currency}] to wallet {to_wallet} from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")

    def buy(self, amount: float, currency: str) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        print(f"buy {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")

    def sell(self, amount: float, currency: str) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        print(f"sell {amount}[{currency}] from {self.__class__.__name__}")
        return ResultOfExchange(status=200, result="ok")


class ExchangeManager(ExchangeManagerABC):
    """
    Exchange Manager for managing exchanges based on coins.

    This class provides methods for transferring, buying, and selling cryptocurrency on the appropriate exchange
     based on the coin provided.
    usage:
        get exchange
        >>> ExchangeManager.get_exchange_from_coins(coin=coin)
        buy currency
        >>> ExchangeManager(coin).buy(10.2)
        sell currency
        >>> ExchangeManager(coin).sell(10.2)
        transfer currency
        >>> ExchangeManager(coin).transfer(to_wallet=user_wallet, amount=10.2)
    """

    @staticmethod
    def get_exchange_from_coins(coin: "Coin") -> ExchangeABC:
        """return exchange class according to given coin"""
        if coin.exchange is None:
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
