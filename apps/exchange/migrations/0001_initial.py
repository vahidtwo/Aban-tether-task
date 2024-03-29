# Generated by Django 4.2.5 on 2023-09-30 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_lifecycle.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coin', '0002_remove_coin_price_coin_icon'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('coin_price', models.FloatField(editable=False, verbose_name='coin price')),
                ('amount', models.FloatField(editable=False, verbose_name='amount')),
                ('total_price', models.FloatField(editable=False, verbose_name='total price')),
                ('transfer_tax', models.FloatField(editable=False, verbose_name='tax')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'init'), (1, 'waiting for send to exchange'), (2, 'send to exchange'), (3, 'retry to send to exchange'), (4, 'success'), (5, 'failed')], default=0, editable=False, verbose_name='status of order')),
                ('failed_result', models.TextField(blank=True, editable=False, null=True, verbose_name='failed result')),
                ('coin', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='coin.coin')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
