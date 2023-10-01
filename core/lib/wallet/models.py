from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from .errors import InsufficientBalance


# We'll be using BigIntegerField by default instead
# of DecimalField for simplicity. This can be configured
# though by setting `WALLET_CURRENCY_STORE_FIELD` in your
# `/confing/base.py`.
CURRENCY_STORE_FIELD = getattr(settings, "WALLET_CURRENCY_STORE_FIELD", models.BigIntegerField)


class BaseModel(models.Model):
    # The date/time of the creation of this record.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class WalletBaseModel(models.Model):
    current_balance = CURRENCY_STORE_FIELD(default=0)

    @property
    def transaction_relation(self):
        return self.transaction_set

    class Meta:
        abstract = True
        verbose_name = _("wallet")
        verbose_name_plural = _("wallets")

    def _deposit(self, value):
        """Deposits a value to the wallet.

        Also creates a new transaction with the deposit
        value.
        """
        self.transaction_relation.create(value=value, total_balance=self.current_balance + value)
        self.current_balance += value
        self.save()

    def _withdraw(self, value):
        """Withdraw's a value from the wallet.

        Also creates a new transaction with the withdraw
        value.

        Should the withdrawn amount is greater than the
        balance this wallet currently has, it raises an
        :mod:`InsufficientBalance` error. This exception
        inherits from :mod:`django.db.IntegrityError`. So
        that it automatically rolls-back during a
        transaction lifecycle.
        """
        if value > self.current_balance:
            raise InsufficientBalance("This wallet has insufficient balance.")

        self.transaction_relation.create(value=-value, total_balance=self.current_balance - value)
        self.current_balance -= value
        self.save()

    @classmethod
    def transfer(cls, src_id, dst_id, value):
        """Transfers an value to another wallet.

        Uses `deposit` and `withdraw` internally.
        """
        with transaction.atomic():
            src_wallet = cls.objects.select_for_update().get(id=src_id)
            dst_wallet = cls.objects.select_for_update().get(id=dst_id)
            src_wallet._withdraw(value=value)
            dst_wallet._deposit(value=value)

    @classmethod
    def deposit(cls, id, value):
        with transaction.atomic():
            wallet = cls.objects.select_for_update().get(id=id)
            wallet._deposit(value=value)

    @classmethod
    def withdraw(cls, id, value):
        with transaction.atomic():
            wallet = cls.objects.select_for_update().get(id=id)
            wallet._withdraw(value=value)


class WalletTransactionBaseModel(BaseModel):
    # The wallet that holds this transaction.
    # set wallet foreign key  for example
    # >>> wallet models.ForeignKey(verbose_name=_("wallet"), to="wallet.Wallet", on_delete=models.CASCADE)
    wallet = ...

    # The value of this transaction.
    value = CURRENCY_STORE_FIELD(default=0)

    # The value of the wallet at the time of this
    # transaction. Useful for displaying transaction
    # history.
    total_balance = CURRENCY_STORE_FIELD(default=0)

    class Meta:
        verbose_name = _("wallet transaction")
        verbose_name_plural = _("wallet transactions")
        abstract = True

    def __str__(self) -> str:
        return f"{self.wallet_id}: {self.value} -> {self.total_balance}"
