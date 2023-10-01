from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.account import views

urlpatterns = [
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # TODO replace it with an other api for better response
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # TODO replace it with an other api for better response
]
