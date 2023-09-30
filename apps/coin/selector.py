from django.db.models import QuerySet

from apps.coin.models import Coin


def fetch_all_coin() -> QuerySet[Coin]:
    return Coin.objects.all()
