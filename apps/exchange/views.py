from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.coin.models import Coin
from apps.exchange.serializers import OrderCreateSerializer
from core.http import Response
from .tasks import try_to_complete_orders
from ..account.models import UserWallet


class OrderView(GenericAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        create an order for a coin
        """
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coin: Coin
        coin = serializer.validated_data["coin"]
        UserWallet.withdraw(id=request.user.wallet.id, value=serializer.validated_data["amount"])
        serializer.save(user=request.user, coin_price=coin.get_price(), exchange=coin.exchange)

        try_to_complete_orders.delay(args=[coin.id])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
