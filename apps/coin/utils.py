from decimal import Decimal

from apps.coin.models import Coin


def get_coin_price_from_market(coin: Coin) -> Decimal:
    """
    fetch price from market for a coin
    """
    return Decimal(4.0)
