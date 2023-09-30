# Generated by Django 4.2.5 on 2023-09-30 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_exchangesite'),
        ('coin', '0003_network_coin_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='exchange',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coins', to='exchange.exchangesite'),
        ),
        migrations.AddField(
            model_name='network',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='network',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='network',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
