from django.urls import path, include


urlpatterns = [
    path("account/", include("apps.account.urls.api")),
    path("coin/", include("apps.coin.urls.api")),
    path("exchange/", include("apps.exchange.urls.api")),
]
