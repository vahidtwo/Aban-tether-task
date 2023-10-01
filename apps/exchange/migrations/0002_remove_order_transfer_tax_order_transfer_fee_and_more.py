# Generated by Django 4.2.5 on 2023-10-01 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transfer_tax',
        ),
        migrations.AddField(
            model_name='order',
            name='transfer_fee',
            field=models.DecimalField(decimal_places=10, default=0, editable=False, max_digits=50, verbose_name='transfer fee'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=10, editable=False, max_digits=50, verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='order',
            name='coin_price',
            field=models.DecimalField(decimal_places=10, editable=False, max_digits=50, verbose_name='coin price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=10, editable=False, max_digits=50, verbose_name='total price'),
        ),
    ]
