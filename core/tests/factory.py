import factory
from factory.fuzzy import FuzzyChoice

from apps.account.models import User
from apps.coin.models import Coin, Network
from apps.exchange.models import Order, ExchangeSite


class NetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Network

    name = factory.Sequence(lambda n: "network%d" % n)


class ExchangeSiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExchangeSite

    name = FuzzyChoice(choices=["kocoin", "binance", "test"])  # todo add other


class CoinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coin

    network = factory.SubFactory(NetworkFactory)
    exchange = factory.SubFactory(ExchangeSiteFactory)
    name = factory.Sequence(lambda n: "coin%d" % n)
    symbol = factory.Sequence(lambda n: "symbol%d" % n)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    coin = factory.SubFactory(CoinFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "username%d" % n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
