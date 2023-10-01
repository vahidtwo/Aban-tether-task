from rest_framework import serializers

from apps.exchange.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("coin", "amount")
