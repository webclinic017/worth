# Generated by Django 3.2.8 on 2022-08-17 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0013_alter_ticker_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='ib_exchange',
            field=models.CharField(choices=[('CASH', 'CASH'), ('STOCK', 'STOCK'), ('BOND', 'BOND'), ('ARCA', 'ARCA'), ('SMART', 'SMART'), ('CME', 'CME'), ('NYM', 'NYM'), ('NYMEX', 'NYMEX'), ('NYBOT', 'NYBOT'), ('NYB', 'NYB'), ('CFE', 'CFE'), ('ECBOT', 'ECBOT')], default='STOCK', max_length=6),
        ),
        migrations.AlterField(
            model_name='market',
            name='yahoo_exchange',
            field=models.CharField(choices=[('CASH', 'CASH'), ('STOCK', 'STOCK'), ('BOND', 'BOND'), ('ARCA', 'ARCA'), ('SMART', 'SMART'), ('CME', 'CME'), ('NYM', 'NYM'), ('NYMEX', 'NYMEX'), ('NYBOT', 'NYBOT'), ('NYB', 'NYB'), ('CFE', 'CFE'), ('ECBOT', 'ECBOT')], default='STOCK', max_length=6),
        ),
    ]
