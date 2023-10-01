from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AdminPasswordChangeForm,
    UserChangeForm as DjangoUserChangeForm,
)
from rest_framework.authtoken.models import TokenProxy

from core.admin.base import BaseAdmin, BaseTabularInline
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
class UserWalletTransactionInline(BaseTabularInline):
    model = UserWalletTransaction


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_filter = ("user", "current_balance")
    inlines = [UserWalletTransactionInline]


class UserCryptoWalletTransactionInline(BaseTabularInline):
    model = UserCryptoWalletTransaction


@admin.register(UserCryptoWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_filter = ("user", "current_balance", "coin")
    inlines = [UserCryptoWalletTransactionInline]
