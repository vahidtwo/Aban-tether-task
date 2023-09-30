from django.db.models import QuerySet
from rest_framework.generics import ListAPIView

from apps.coin.filters import CoinFilter
from apps.coin.models import Coin
from apps.coin.selector import fetch_all_coin
from apps.coin.serializers import CoinListSerializer
from core.pagination import CustomPagination


class CoinListView(ListAPIView):
    pagination_class = CustomPagination
    filterset_class = CoinFilter
    serializer_class = CoinListSerializer

    def get_queryset(self) -> QuerySet[Coin]:
        return fetch_all_coin()
