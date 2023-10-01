import time
import uuid

from celery import shared_task
from django.db import transaction
from django.db.models import Sum, Q
from rest_framework import status

from apps.account.models import UserCryptoWallet
from apps.coin.models import Coin
from apps.exchange.integration.exchanges import ExchangeManager
from apps.exchange.models import Order
from config.celery import check_task_is_running


@shared_task
def try_to_complete_orders(coin_id: uuid.uuid4):
    # TODO lock data and use better one manager to check just one consumer run compute_task task
    # or implement a watchdog service to check it
    # for limitation of time this implement like this
    while check_task_is_running("apps.exchange.tasks.compute_task"):
        time.sleep(0.5)
    compute_task.delay(coin_id)


@shared_task
def compute_task(coin_id: uuid.uuid4):
    """
    Complete orders accord to requested coin on orders
    the orders send to exchange when aggregate of order-price rich to 10$
    """
    orders = Order.objects.exclude(
        status__in=[Order.OrderStatus.BUY_FROM_EXCHANGE, Order.OrderStatus.ADDED_TO_USER_WALLET]
    )
    sum_of_order = orders.aggregate(sum=Sum("total_price") - Sum("transfer_fee"))["sum"] or 0
    if orders.exists() and sum_of_order >= 10:  # TODO it must get limit of order from gateway of related exchange
        with transaction.atomic():
            coin = Coin.objects.get(id=coin_id)
            orders = orders.select_for_update()
            orders.update(status=Order.OrderStatus.SEND_TO_EXCHANGE)
            result = ExchangeManager(coin).buy(
                amount=sum_of_order
            )  # TODO it must be async function that must await here
            match result.status_code:
                case status.HTTP_200_OK:
                    orders.update(status=Order.OrderStatus.BUY_FROM_EXCHANGE)
                case status.HTTP_429_TOO_MANY_REQUESTS:
                    # TODO use token buket algorithm
                    # check https://www.krakend.io/docs/throttling/token-bucket/
                    orders.update(status=Order.OrderStatus.RETRY_TO_SEND_TO_EXCHANGE)
                case _:
                    orders.update(status=Order.OrderStatus.FAILED, failed_result=str(result))
            if result.status_code == status.HTTP_200_OK:
                add_complete_orders_to_user_wallets.delay()


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
