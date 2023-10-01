from decimal import Decimal

from apps.coin.models import Coin
from apps.exchange.integration.exchange_schema import ExchangeABC


def get_transfer_tax(coin: Coin, amount: Decimal) -> Decimal:
    """
    fetch transfer tax from market for a coin
    """
    return Decimal(0.001)


def buy_from_exchange(coin: Coin, amount: Decimal, exchange: ExchangeABC) -> Decimal:
    """
    buy currency from exchange for a coin
    this function implement in exchanges.py by Exchange classes
    """
    raise NotImplementedError("this function implement in exchanges.py by Exchange clasess")
