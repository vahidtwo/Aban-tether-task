from django.urls import path
from .. import views

urlpatterns = [
    path("", views.CoinListView.as_view(), name="coin.list"),
]
