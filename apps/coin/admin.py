from django.contrib import admin

from apps.coin.models import Coin, Network
from core.admin.base import BaseAdmin


@admin.register(Coin)
class CoinAdmin(BaseAdmin):
    list_display = ("name", "symbol", "get_price")


@admin.register(Network)
class NetworkAdmin(BaseAdmin):
    list_display = ("name",)
