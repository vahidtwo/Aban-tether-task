from decimal import Decimal

from apps.coin.models import Coin


def get_coin_price_from_market(coin: Coin) -> Decimal:
    """
    fetch price from market for a coin
    """
    return Decimal(4.0)


def get_transfer_tax(coin: Coin, amount: Decimal) -> Decimal:
    """
    fetch transfer tax from market for a coin
    """
    return Decimal(0.001)
