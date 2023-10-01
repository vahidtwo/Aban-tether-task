from decimal import Decimal

from apps.coin.models import Coin
from apps.exchange.integration.exchange_schema import ExchangeABC


def buy_from_exchange(coin: Coin, amount: Decimal, exchange: ExchangeABC) -> Decimal:
    """
    buy currency from exchange for a coin
    this function implement in exchanges.py by Exchange classes
    """
    raise NotImplementedError("this function implement in exchanges.py by Exchange clasess")
