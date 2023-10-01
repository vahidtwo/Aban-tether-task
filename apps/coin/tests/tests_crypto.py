from decimal import Decimal
from unittest import mock

from rest_framework.reverse import reverse

from django.test import TransactionTestCase

from apps.coin.models import Coin
from core.tests import factory as factories


class CoinTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.network = factories.NetworkFactory.create()
        self.exchange = factories.ExchangeSiteFactory.create()
        self.coins = factories.CoinFactory.create_batch(10, network=self.network, exchange=self.exchange)

    def test_get_coins(self):
        url = reverse("coin.list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(len(data), 10)

    def test_get_coins_with_pagination(self):
        url = reverse("coin.list")
        response = self.client.get(url, data={"size": 1})
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(len(data["results"]), 1)
        response = self.client.get(url, data={"size": 1, "p": 10})
        data = response.json()
        self.assertEquals(len(data["results"]), 1)
        self.assertIsNone(data["next"])

    def test_get_coin_with_fetch_all_coin_mock(self):
        with mock.patch("apps.coin.views.fetch_all_coin") as query_set:
            query_set.return_value = Coin.objects.all()[:3]
            url = reverse("coin.list")
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)
            data = response.json()
            self.assertEquals(len(data), 3)
            query_set.reset_mock()

    def test_get_coin_with_coin_price_mock(self):
        with mock.patch("apps.coin.utils.get_coin_price_from_market") as price:
            price.return_value = Decimal(1.55)
            url = reverse("coin.list")
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)
            data = response.json()
            self.assertEquals(data[0]["price"], 1.55)
            price.reset_mock()

    def test_get_coin_with_filter_coin(self):
        factories.CoinFactory.create_batch(10, network=self.network, exchange=self.exchange)
        url = reverse("coin.list")
        response = self.client.get(url, data={"q": "0"})
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(len(data), 2)
