from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView

from apps.coin.models import Coin
from apps.exchange.serializers import OrderCreateSerializer
from core.http import Response
from core.permissions import IsAuthenticatedCustomer
from .tasks import try_to_complete_orders
from ..account.models import UserWallet


class OrderView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticatedCustomer]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        create an order for a coin
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        coin: Coin
        coin = serializer.validated_data["coin"]
        UserWallet.withdraw(
            id=self.request.user.wallet.id, value=coin.get_buyer_price(serializer.validated_data["amount"])
        )
        serializer.save(user=self.request.user, coin_price=coin.get_price(), exchange=coin.exchange)

        try_to_complete_orders.delay(coin.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
