# Generated by Django 4.2.5 on 2023-09-30 13:26

import apps.exchange.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_alter_order_options_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeSite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='name')),
                ('icon', models.ImageField(upload_to=apps.exchange.models.get_exchange_site_icon, verbose_name='icon')),
            ],
            options={
                'verbose_name': 'exchange site',
                'verbose_name_plural': 'exchange sites',
            },
        ),
    ]
