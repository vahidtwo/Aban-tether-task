from django.contrib import admin

from apps.exchange.models import Order, ExchangeSite
from core.admin.base import BaseAdmin
from core.admin.mixing import ThumbnailAdminMixing


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = (
        "user",
        "coin",
        "coin_price",
        "amount",
        "total_price",
        "transfer_fee",
        "status",
    )
    list_filter = ("status", "coin")


@admin.register(ExchangeSite)
class ExchangeSiteAdmin(BaseAdmin, ThumbnailAdminMixing):
    thumbnail_field_name = "icon"
    list_filter = ("name",)
