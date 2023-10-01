from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_CREATE

from core.models.base import TimeStampedBaseModel, BaseModel


class Order(LifecycleModelMixin, TimeStampedBaseModel):
    """
    Model representing an order.

    Attributes:
        OrderStatus (enum): Enum for order statuses.
        user (User): The user who placed the order.
        coin (Coin): The cryptocurrency associated with the order.
        coin_price (float): The price of the cryptocurrency at the time of the order.
        amount (float): The amount of cryptocurrency in the order.
        total_price (float): The total price of the order.
        transfer_tax (float): The tax associated with the order.
        status (int): The status of the order.
        failed_result (str): Details of any failure associated with the order.
        exchange (ExchangeSite): The exchange site used for the order (nullable).

    Hooks:
        calc_total_price_and_transfer_tax(): Calculates total price and transfer tax before order creation.
    """

    class OrderStatus(models.IntegerChoices):
        INIT = 0, _("init")
        WAITING_FOR_SEND_TO_EXCHANGE = 1, _("waiting for send to exchange")
        SEND_TO_EXCHANGE = 2, _("send to exchange")
        RETRY_TO_SEND_TO_EXCHANGE = 3, _("retry to send to exchange")
        BUY_FROM_EXCHANGE = 4, _("buy from exchange")
        FAILED = 5, _("failed")
        ADDED_TO_USER_WALLET = 6, _("added to user wallet")

    user = models.ForeignKey("account.User", on_delete=models.PROTECT, related_name="orders", editable=False)
    coin = models.ForeignKey("coin.Coin", on_delete=models.PROTECT, related_name="orders", editable=False)
    coin_price = models.DecimalField(max_digits=50, decimal_places=10, verbose_name=_("coin price"), editable=False)
    amount = models.DecimalField(max_digits=50, decimal_places=10, verbose_name=_("amount"), editable=False)
    total_price = models.DecimalField(max_digits=50, decimal_places=10, verbose_name=_("total price"), editable=False)
    transfer_fee = models.DecimalField(max_digits=50, decimal_places=10, verbose_name=_("transfer fee"), editable=False)
    status = models.PositiveSmallIntegerField(
        default=OrderStatus.INIT,
        choices=OrderStatus.choices,
        editable=False,
        verbose_name=_("status of order"),
        db_index=True,
    )
    failed_result = models.TextField(null=True, blank=True, verbose_name=_("failed result"), editable=False)
    exchange = models.ForeignKey(
        "exchange.ExchangeSite", null=True, blank=True, on_delete=models.PROTECT, related_name="orders", editable=False
    )

    @hook(BEFORE_CREATE)
    def calc_total_price_and_transfer_tax(self):
        """
        Calculate total price and transfer tax before order creation.
        """
        from apps.coin.utils import get_transfer_tax

        self.transfer_fee = get_transfer_tax(self.coin, self.amount)
        self.total_price = (self.coin_price * self.amount) + self.transfer_fee

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


def get_exchange_site_icon(exchange_site: "ExchangeSite", file_name: str) -> str:
    """
    Generate the upload path for an exchange site's icon image.

    Args:
        exchange_site (ExchangeSite): The exchange site for which the icon is being uploaded.
        file_name (str): The original file name of the uploaded image.

    Returns:
        str: The upload path for the exchange site's icon image.
    """
    import pathlib

    file_extension = pathlib.Path(file_name).suffix

    return f"exchange_site/{exchange_site.name}.{file_extension}"


class ExchangeSite(BaseModel):
    """
    Model representing an exchange site.

    Attributes:
        name (str): The name of the exchange site (unique).
        icon (ImageField): The icon image for the exchange site.
    """

    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"), db_index=True)
    icon = models.ImageField(verbose_name=_("icon"), upload_to=get_exchange_site_icon)

    class Meta:
        verbose_name = _("exchange site")
        verbose_name_plural = _("exchange sites")
