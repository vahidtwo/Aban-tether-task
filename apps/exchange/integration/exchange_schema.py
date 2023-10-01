from decimal import Decimal
from abc import ABC, abstractmethod
from dataclasses import dataclass

from apps.coin.models import Coin
from apps.exchange.integration import ResultOfExchange


class ExchangeABC(ABC):
    api_key: str = ...
    gate_way: str = ...

    @abstractmethod
    def transfer(self, to_wallet: str, amount: Decimal, currency: str) -> ResultOfExchange:
        """transfer amount of a currency from one wallet to another wallet"""
        # TODO it must be async function
        ...

    @abstractmethod
    def buy(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        # TODO it must be async function
        ...

    @abstractmethod
    def sell(self, amount: Decimal, currency: str) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        # TODO it must be async function
        ...


class ExchangeManagerABC(ABC):
    """
     Exchange Manager for managing exchanges based on coins.

    This class provides methods for transferring, buying, and selling cryptocurrency on the appropriate exchange based on the coin provided.

    Usage:
    - To get the exchange for a given coin: ExchangeManager.get_exchange_from_coins(coin)
    - To transfer currency: ExchangeManager(coin).transfer(to_wallet, amount)
    - To buy currency: ExchangeManager(coin).buy(amount)
    - To sell currency: ExchangeManager(coin).sell(amount)

    Attributes:
        coin (Coin): The coin for which the exchange operations will be performed.
    """

    def __init__(self, coin: Coin):
        self.coin = coin

    @staticmethod
    @abstractmethod
    def get_exchange_from_coins(coin: Coin) -> ExchangeABC:
        """return exchange class according to given coin"""
        ...

    def transfer(self, to_wallet: str, amount: Decimal) -> ResultOfExchange:
        """transfer amount of a currency from our wallet on exchange to another wallet"""
        # TODO it must be async function
        return self.get_exchange_from_coins(self.coin).transfer(
            to_wallet=to_wallet, amount=amount, currency=self.coin.symbol
        )

    def buy(self, amount: Decimal) -> ResultOfExchange:
        """buy amount of currency from exchange"""
        # TODO it must be async function
        return self.get_exchange_from_coins(self.coin).buy(amount=amount, currency=self.coin.symbol)

    def sell(self, amount: Decimal) -> ResultOfExchange:
        """sell amount of currency from exchange"""
        # TODO it must be async function
        return self.get_exchange_from_coins(self.coin).buy(amount=amount, currency=self.coin.symbol)
