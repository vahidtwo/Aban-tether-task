import factory

from apps.coin import models


class CoinFactory(factory.Factory):
    class Meta:
        model = models.Coin


class NetworkFactory(factory.Factory):
    class Meta:
        model = models.Network
