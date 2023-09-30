def get_transfer_tax(coin: "Coin", amount: float) -> float:
    """
    fetch transfer tax from market for a coin
    """
    return 0.001


def buy_from_exchange(coin: "Coin", amount: float, exchange: "ExchangeABC") -> float:
    """
    buy currency from exchange for a coin
    this function implement in exchanges.py by Exchange classes
    """
    raise NotImplementedError("this function implement in exchanges.py by Exchange clasess")
