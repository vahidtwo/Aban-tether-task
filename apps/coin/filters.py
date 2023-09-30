import django_filters
from django.db.models import Q
from django_filters import CharFilter

from apps.coin.models import Coin


class CoinFilter(django_filters.FilterSet):
    q = CharFilter(method="name_filter")

    class Meta:
        model = Coin
        fields = []

    def name_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(symbol__icontains=value))
