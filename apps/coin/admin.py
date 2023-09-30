from core.admin.base import BaseAdmin


# Register your models here.
class CoinAdmin(BaseAdmin):
    list_display = ["name", "symbol", "get_price"]
