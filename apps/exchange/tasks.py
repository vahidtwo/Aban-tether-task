from celery import shared_task
from django.db import transaction
from django.db.models import Sum, Q
from rest_framework import status

from apps.account.models import UserCryptoWallet
from apps.coin.models import Coin
from apps.exchange.exchanges import ExchangeManager
from apps.exchange.models import Order


@shared_task
def try_to_complete_orders():
    # TODO lock data and use one manager to check just one consumer run this task
    # or implement a watchdog service to check it
    # for limitation of time this implement like this
    """
    Complete orders accord to requested coin on orders
    the orders send to exchange when aggregate of order-price rich to 10$
    """
    with transaction.atomic():
        coins = Coin.objects.annotate(
            orders_price=Sum(
                "orders__total_price",
                filter=~Q(
                    order__status__in=[Order.OrderStatus.BUY_FROM_EXCHANGE, Order.OrderStatus.ADDED_TO_USER_WALLET]
                ),
            ).filter(
                orders_price__gre=10.0  # TODO it must get limit of order from gateway of related exchange
            )
        )
        for coin in coins.iterator():  # TODO it must use multy thread
            orders = coin.orders.filter(
                status__in=[Order.OrderStatus.BUY_FROM_EXCHANGE, Order.OrderStatus.ADDED_TO_USER_WALLET]
            )
            orders.update(status=Order.OrderStatus.SEND_TO_EXCHANGE)
            result = ExchangeManager(coin).buy(amount=coin.orders_price)
            match result.status:
                case status.HTTP_200_OK:
                    orders.update(status=Order.OrderStatus.BUY_FROM_EXCHANGE)
                    add_complete_orders_to_user_wallets.delay()
                case status.HTTP_429_TOO_MANY_REQUESTS:
                    # TODO use token buket algorithm
                    # check https://www.krakend.io/docs/throttling/token-bucket/
                    orders.update(status=Order.OrderStatus.RETRY_TO_SEND_TO_EXCHANGE)
                case _:
                    orders.update(status=Order.OrderStatus.FAILED, failed_result=str(result))


@shared_task
def add_complete_orders_to_user_wallets():
    """add amount of order to user crypto wallet
    the order status change to ADDED_TO_USER_WALLET
    """
    orders = Order.objects.filter(status=Order.OrderStatus.BUY_FROM_EXCHANGE)
    complete_orders = []
    for order in orders.iterator():
        with transaction.atomic():
            user = order.user
            user_crypto_wallet = user.user_cryptos.get_or_create(user=user, coin=order.coin)[0]
            UserCryptoWallet.deposit(user_crypto_wallet.id, order.amount)
            order.status = Order.OrderStatus.ADDED_TO_USER_WALLET
            complete_orders.append(order)
    Order.objects.bulk_update(complete_orders, ["status"])
