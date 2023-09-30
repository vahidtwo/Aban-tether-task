from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.coin.models import Coin


class CoinListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Coin
        fields = ("id", "name", "symbol", "icon", "price")

    @extend_schema_field(serializers.IntegerField())
    def get_price(self, coin: Coin):
        return coin.get_price()
