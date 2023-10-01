from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AdminPasswordChangeForm,
    UserChangeForm as DjangoUserChangeForm,
)
from django.core.paginator import Paginator
from django.db.models import Sum
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_admin_inline_paginator.admin import TabularInlinePaginated
from rest_framework.authtoken.models import TokenProxy

from core.admin.base import BaseAdmin, BaseTabularInline
from core.lib.wallet.models import WalletBaseModel
from . import models
from .models import UserWallet, UserWalletTransaction, UserCryptoWalletTransaction, UserCryptoWallet


class UserChangeForm(DjangoUserChangeForm):
    class Meta(DjangoUserChangeForm.Meta):
        pass


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        fields = ("email",)


@admin.register(models.User)
class UserAdmin(UserAdmin, BaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("id", "full_name", "email", "is_staff")
    search_fields = ("email",)
    list_filter = ("first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = tuple()
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "username",
                    "is_staff",
                    "password",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                    "username",
                    "email",
                    "is_staff",
                )
            },
        ),
    )


# TODO it must readonly current balance and add feature to admin just can add wallet transaction
# in following admin models:
#    UserWalletTransactionInline   UserWalletAdmin   UserCryptoWalletTransactionInline  UserWalletAdmin


class WalletTransactionPaginatorInline(TabularInlinePaginated):
    extra = 1
    readonly_fields = ("total_balance",)
    per_page = 10

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_max_num(self, request, obj: WalletBaseModel = None, **kwargs):
        paginator = Paginator(obj.transaction_relation.all(), self.per_page)
        page = paginator.get_page(request.GET.get("page"))
        if page.object_list.count() % self.per_page > 0:
            return page.object_list.count() + 1
        return self.per_page + 1


class UserWalletTransactionInline(WalletTransactionPaginatorInline):
    model = UserWalletTransaction


class UserWalletBaseAdmin(admin.ModelAdmin):
    list_display = ("user", "current_balance")
    search_fields = ("user__first_name", "user__last_name")
    readonly_fields = ("current_balance",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        wallet = self.model.objects.get(pk=form.instance.pk)
        transactions = wallet.transaction_relation.all()
        sum_transactions = transactions.aggregate(Sum("value"))["value__sum"] or 0
        wallet.current_balance = sum_transactions
        wallet.save()
        if transactions.exists():
            latest_transaction = transactions.last()
            latest_transaction.total_balance = wallet.current_balance
            latest_transaction.save()


@admin.register(UserWallet)
class UserWalletAdmin(UserWalletBaseAdmin):
    inlines = [UserWalletTransactionInline]


class UserCryptoWalletTransactionInline(WalletTransactionPaginatorInline):
    model = UserCryptoWalletTransaction


@admin.register(UserCryptoWallet)
class UserWalletAdmin(UserWalletBaseAdmin):
    list_filter = ("user", "current_balance", "coin")
    inlines = [UserCryptoWalletTransactionInline]
