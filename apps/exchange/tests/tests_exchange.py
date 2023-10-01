from unittest import TestCase

from django.test import TransactionTestCase


# The test not implement for time limit but i write some test in coin app
class OrderTestCase(TransactionTestCase):
    def setUp(self) -> None:
        # TODO add some order with factory
        pass

    def test_create_order(self):
        # TODO test create order
        pass

    def test_create_order_with_mock_celery(self):
        pass

    def test_create_order_with_mock_wallet_withdrow(self):
        pass

    # TODO other tests


class ExchangeTestCase(TestCase):
    pass
    # TODO test implemet exchange
