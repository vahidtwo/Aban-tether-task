from django.db import models

from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


def get_coin_image(coin: "Coin", file_name: str) -> str:
    """
    Generate the upload path for a coin's icon image.

    Args:
        coin (Coin): The coin for which the image is being uploaded.
        file_name (str): The original file name of the uploaded image.

    Returns:
        str: The upload path for the coin's icon image.
    """
    import pathlib

    file_extension = pathlib.Path(file_name).suffix

    return f"coin/{coin.name}.{file_extension}"


class Coin(BaseModel):
    """
    Coin model representing a cryptocurrency.

    Attributes:
        name (str): The name of the cryptocurrency (unique).
        symbol (str): The symbol of the cryptocurrency (unique).
        icon (ImageField): The icon image for the cryptocurrency.
        network (Network): The network associated with the coin.
        exchange (ExchangeSite): The exchange site associated with the coin (nullable).

    Methods:
        get_price(): Fetches the price of the coin from the market.

    """

    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"), db_index=True)
    symbol = models.CharField(max_length=10, unique=True, verbose_name=_("symbol"), db_index=True)
    icon = models.ImageField(null=True, blank=True, verbose_name=_("icon"), upload_to=get_coin_image)
    # TODO: network can be Many-to-many if one coin can act on multiple network search
    network = models.ForeignKey("coin.Network", on_delete=models.PROTECT, related_name="coins")
    exchange = models.ForeignKey(
        "exchange.ExchangeSite", null=True, blank=True, on_delete=models.PROTECT, related_name="coins"
    )

    def get_price(self) -> Decimal:
        """
        Fetch the price of the coin from the market.

        Returns:
            float: The current price of the coin.
        """
        from apps.coin.utils import get_coin_price_from_market

        return get_coin_price_from_market(self)

    def get_buyer_price(self, amount: Decimal) -> Decimal:
        from apps.coin.utils import get_transfer_tax

        return (self.get_price() * amount) + get_transfer_tax(self, amount)

    get_price.short_description = _("price")

    class Meta:
        verbose_name = _("coin")
        verbose_name_plural = _("coins")


class Network(BaseModel):
    """
    Network model representing a cryptocurrency network.

    Attributes:
        name (str): The name of the cryptocurrency network (unique).

    """

    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"), db_index=True)

    class Meta:
        verbose_name = _("network")
        verbose_name_plural = _("networks")
