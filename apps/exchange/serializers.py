from rest_framework import serializers

from apps.coin.models import Coin
from apps.exchange.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    coin = serializers.PrimaryKeyRelatedField(queryset=Coin.objects.all())
    amount = serializers.DecimalField(decimal_places=10, label="Amount", max_digits=50)

    class Meta:
        model = Order
        fields = ["coin", "amount"]
