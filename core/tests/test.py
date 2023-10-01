from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class TokenAPIClient(APIClient):
    def _set_token(self, user: User = None, user_id=None):
        if user is None:
            user = User.objects.get(user_id=user_id)
        self.credentials(HTTP_AUTHORIZATION="Bearer {}".format(user.tokens["access"]))

    def remove_token(self):
        self.credentials()


class TokenAPITestCases(APITestCase, TransactionTestCase):
    client_class = TokenAPIClient
    fake = Faker(locale="fa_IR")

    def login(self, user: User = None):
        """
        Set user credentials
        if user not set create a default user
        """
        if user is None:
            user = User.objects.get_or_create(
                username=self.fake.user_name(),
                email=self.fake.email(),
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
            )
        self.client._set_token(user=user)

    def logout(self):
        """
        remove user credentials
        """
        self.client.remove_token()
