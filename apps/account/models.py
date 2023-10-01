from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE

from apps.account.managers import UserManager
from core.lib.wallet.models import WalletTransactionBaseModel, WalletBaseModel
from core.models.base import TimeStampedBaseModel
from core.models.user import AbstractUser


class User(LifecycleModelMixin, AbstractUser):
    """
    User model representing individuals.

    This model represents users of the system, including their roles and associated wallets.

    Attributes:
        UserRole (enum): Enum for user roles, including CUSTOMER, SUPPORT, and ADMIN.
        role (int): The user's role (default: CUSTOMER).
        full_name (property): The user's full name.
        objects (UserManager): The custom manager for User objects.

    Methods:
        tokens(): Generates and returns jwt authentication tokens for the user.

    Lifecycle Hooks:
        create_wallet_for_customer(): Creates a wallet for the user after creation if the role is CUSTOMER.
    """

    class UserRole(models.IntegerChoices):
        CUSTOMER = 1, _("customer")
        SUPPORT = 2, _("support")
        ADMIN = 3, _("admin")

    role = models.PositiveSmallIntegerField(default=UserRole.CUSTOMER, choices=UserRole.choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @cached_property
    def full_name(self):
        return self.get_full_name()

    full_name.short_description = _("full name")
    objects = UserManager()

    @hook(AFTER_CREATE, when="role", is_now=UserRole.CUSTOMER)
    def create_wallet_for_customer(self):
        """Create a wallet for the user before creation if the role is CUSTOMER."""
        UserWallet.objects.create(user=self)

    def tokens(self):
        """
        Generate and return authentication tokens for the user.

        Returns:
            dict: A dictionary containing the refresh and access tokens.
        """
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class UserWallet(WalletBaseModel):
    """
    Wallet model associated with a user.

    This model represents a wallet associated with a user account.

    Attributes:
        user (User): The user associated with this wallet.

    """

    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.PROTECT, related_name="wallet")

    class Meta:
        verbose_name = _("user wallet")
        verbose_name_plural = _("user wallets")

    @property
    def transaction_relation(self):
        return self.userwallettransaction_set


class UserWalletTransaction(WalletTransactionBaseModel):
    """
    Transaction model for user wallets.

    This model represents transactions associated with user wallets.

    Attributes:
        wallet (UserWallet): The user wallet associated with this transaction.

    """

    wallet = models.ForeignKey("account.UserWallet", verbose_name=_("wallet"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("user wallet transaction")


class UserCryptoWallet(LifecycleModelMixin, TimeStampedBaseModel, WalletBaseModel):
    """
    Crypto wallet model associated with a user.

    This model represents a crypto wallet associated with a user account.

    Attributes:
        user (User): The user associated with this crypto wallet.
        coin (Coin): The cryptocurrency coin associated with this crypto wallet.

    """

    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.PROTECT, related_name="user_cryptos")
    coin = models.ForeignKey("coin.Coin", verbose_name=_("coin"), on_delete=models.PROTECT, related_name="users_crypto")

    # wallet can be replaced with other model if we create actual crypto wallet for users,
    # and we must add some functionality to transfer crypto from exchange to user wallet
    # in this case we must remove WalletBaseModel ,
    # and use Exchange.transfer in exchange.tasks.add_complete_orders_to_user_wallets
    class Meta:
        verbose_name = _("user crypto")
        verbose_name_plural = _("user cryptos")

    @property
    def transaction_relation(self):
        return self.usercryptowallettransaction_set


class UserCryptoWalletTransaction(WalletTransactionBaseModel):
    """
    Transaction model for user crypto wallets.

    This model represents transactions associated with user crypto wallets.

    Attributes:
        wallet (UserCryptoWallet): The user crypto wallet associated with this transaction.


    """

    wallet = models.ForeignKey("account.UserCryptoWallet", verbose_name=_("wallet"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("user crypto wallet transaction")
